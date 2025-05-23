from ..config import Config
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session, current_app
from flask_login import login_user, logout_user, current_user, login_required
import json

from ..extensions import db
from ..models.progress import Progress  # Импортируем модель Progress

Iquiz = Blueprint('Iquiz', __name__)

def load_interactive_quiz(game_name):
    try:
        json_path = Config.get_json_path(game_name)
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f'Ошибка загрузки интерактивного квиза: {e}')
        return None

def save_progress(progress, user_id, game_name, scene_id, total_points, type_id):
    if progress:
        progress.progress_scene = scene_id
        progress.progress_ball = total_points
    else:
        progress = Progress(
            user_id=user_id,
            game_name=game_name,
            progress_scene=scene_id,
            progress_ball=total_points,
            type_id=type_id
        )
        db.session.add(progress)
    db.session.commit()


@Iquiz.route('/Iquiz/<int:type_id>/<game_name>', methods=['GET', 'POST'])
@login_required
def interactive_quiz(type_id, game_name):
    quiz_data = load_interactive_quiz(game_name)
    if not quiz_data:
        return "Данные квиза не найдены", 404

    progress = Progress.query.filter_by(user_id=current_user.id, game_name=game_name, type_id=type_id).first()

    if request.method == 'GET' and progress and not session.get(f'confirmed_{game_name}_{type_id}'):
        quiz_finished = (progress.progress_scene == 0 or progress.progress_scene is None) and progress.progress_ball > 0
        return render_template(
            'Iquiz/confirm_continue.html',
            game_name=game_name,
            total_points=progress.progress_ball,
            quiz_finished=quiz_finished
        )

    if progress:
        total_points = progress.progress_ball or 0
        saved_scene = progress.progress_scene if progress.progress_scene not in (None, 0) else quiz_data.get(
            'start_scene', 1)
    else:
        total_points = 0
        saved_scene = quiz_data.get('start_scene', 1)


    if saved_scene in (0, None):
        # Игра закончена — показываем результаты
        session.pop(f'confirmed_{game_name}_{type_id}', None)
        return render_template('Iquiz/results.html', total_points=total_points, game_name=game_name)

    if request.method == 'POST':
        if 'restart' in request.form:
            if progress:
                db.session.delete(progress)
                db.session.commit()
            session.pop(f'confirmed_{game_name}_{type_id}', None)
            total_points = 0
            saved_scene = quiz_data.get('start_scene', 1)

        else:
            selected_answer = request.form.get('answer')
            if selected_answer is not None:
                selected_answer = int(selected_answer)
                current_scene = quiz_data['scenes'][saved_scene - 1]
                answer = current_scene['answers'][selected_answer]

                total_points += answer['points']
                next_scene_id = answer['next_scene']

                save_progress(progress, current_user.id, game_name, next_scene_id, total_points, type_id)

                if next_scene_id is None:
                    session.pop(f'confirmed_{game_name}_{type_id}', None)
                    return render_template('Iquiz/results.html', total_points=total_points, game_name=game_name)

                saved_scene = next_scene_id

    return render_template(f'Iquiz/{game_name}.html',
                           game_name=game_name,
                           quiz_data=quiz_data,
                           saved_scene=saved_scene,
                           total_points=total_points)




@Iquiz.route('/Iquiz/save_progress', methods=['POST'])
@login_required
def save_progress_route():
    data = request.get_json()
    game_name = data.get("game_name")
    current_scene = data.get("current_scene")
    total_points = data.get("total_points")
    type_id = data.get("type_id", 2)
    end_game = data.get("end_game", False)  # Флаг для завершения игры

    if not game_name:
        return jsonify({"error": "Отсутствует имя игры"}), 400
    if total_points is None:
        return jsonify({"error": "Отсутствуют очки"}), 400

    # Находим прогресс текущего пользователя для данной игры
    progress = Progress.query.filter_by(user_id=current_user.id, game_name=game_name, type_id=type_id).first()

    # Используем универсальную функцию для сохранения прогресса
    save_progress(progress, current_user.id, game_name, current_scene, total_points, type_id)

    if end_game:
        if progress:
            progress.progress_scene = 0
            progress.progress_ball = total_points
            db.session.commit()
        session.pop(f'confirmed_{game_name}_{type_id}', None)
        return jsonify({"message": "Прогресс сохранён, игра завершена",
                        "redirect": url_for('Iquiz.interactive_quiz', type_id=type_id, game_name=game_name)})

    return jsonify({"message": "Прогресс сохранён", "current_scene": current_scene, "total_points": total_points})




@Iquiz.route('/Iquiz/get_scene/<int:scene_id>/<game_name>', methods=['GET'])
@login_required
def get_scene(scene_id, game_name):
    quiz_data = load_interactive_quiz(game_name)
    if not quiz_data:
        return jsonify({"error": "Данные квиза не найдены"}), 404
    scene = next((s for s in quiz_data['scenes'] if s['id'] == scene_id), None)
    if not scene:
        return jsonify({"error": "Сцена не найдена"}), 404
    # Получаем текущие очки пользователя
    progress_record = Progress.query.filter_by(user_id=current_user.id, game_name=game_name).first()
    current_points = progress_record.progress_ball if progress_record else 0
    return jsonify({"scene": scene, "current_points": current_points})



@Iquiz.route('/Iquiz/exit', methods=['POST'])
@login_required
def exit_quiz():
    data = request.get_json()
    game_name = data.get("game_name")
    current_scene = data.get("current_scene")  # может быть None
    total_points = data.get("total_points")
    try:
        type_id = int(data.get("type_id", 2))
    except ValueError:
        type_id = 2


    if not game_name:
        return jsonify({"error": "Отсутствуют необходимые данные"}), 400

    progress_record = Progress.query.filter_by(user_id=current_user.id, game_name=game_name,
                                               type_id=type_id).first()

    if progress_record:
        if current_scene is not None:
            progress_record.progress_scene = current_scene
        progress_record.progress_ball = total_points
    else:
        progress_record = Progress(
            user_id=current_user.id,
            game_name=game_name,
            progress_scene=current_scene if current_scene is not None else 0,
            progress_ball=total_points,
            type_id=type_id
        )
        db.session.add(progress_record)

    db.session.commit()
    session.pop(f'confirmed_{game_name}_{type_id}', None)

    return jsonify({"message": "Прогресс сохранён", "redirect": url_for('main.show')})





@Iquiz.route('/Iquiz/continue', methods=['POST'])
@login_required
def continue_or_restart():
    data = request.get_json()
    game_name = data.get("game_name")
    action = data.get("action")

    progress = Progress.query.filter_by(user_id=current_user.id, game_name=game_name).first()
    type_id = progress.type_id if progress else 2

    if action == "continue":
        if progress:
            session[f'confirmed_{game_name}_{type_id}'] = True  # <-- Ставим флаг, что выбрал продолжить
            return jsonify({
                "success": True,
                "redirect_url": url_for('Iquiz.interactive_quiz', type_id=type_id, game_name=game_name)
            })
        else:
            return jsonify({"success": False, "message": "Прогресс не найден"})

    elif action == "restart":
        if progress:
            db.session.delete(progress)
            db.session.commit()
        session.pop(f'confirmed_{game_name}_{type_id}', None)  # <-- Убираем флаг
        return jsonify({
            "success": True,
            "redirect_url": url_for('Iquiz.interactive_quiz', type_id=type_id, game_name=game_name)
        })

    return jsonify({"success": False, "message": "Неизвестное действие"})




