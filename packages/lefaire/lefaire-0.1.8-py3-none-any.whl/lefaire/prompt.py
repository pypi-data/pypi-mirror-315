import typer
import sys

add_select = "À quel projet ajouter une tâche ?"
create_name = "Quel est le nom de ce nouveau projet ?"
delete_select_all = "Quel projet voulez-vous supprimer ?"
delete_select = "Dans quel projet se trouve la tâche à supprimer ?"
description = "Comment décrire le projet ?"
done_select = "À quel projet appartient la tâche à terminer ?"
done_rank = "Quel est le rang de la tâche à terminer ?"
due_date = "Quelle est la date butoir pour ce projet (JJ/MM/AAA HH:MM:SS) ?"
info_select = "Entrer le Numéro ou nom du projet à consulter | (C)réer un projet"
modify_rank = "Quel est le rang de la tâche à modifier ?"
modify_select = "Quel projet est à modifier ?"
modify_task_select = "À quel projet appartient la tâche à modifier ?"
move_rank = "Quel est le rang de la tâche à déplacer ?"
move_select = "À quel projet appartient la tâche à déplacer ?"
task_body = "En quoi consiste cette tâche ?"
relocate_new = "Quel est le nouvel identifiant du projet"
relocate_select = "Quel projet est à deplacer ?"
rename_name = "Quel est le nouveau nom de ce projet ?"
rename_select = "Quel projet est à renommer ?"
start_rank = "Quel est le rang de la tâche à commencer ?"
start_select = "À quel projet appartient la tâche à commencer ?"
undo_rank = "Quel est le rang de la tâche à retravailler ?"
undo_select = "À quel projet appartient la tâche à retravailler ?"
unstart_rank = "Quel est le rang de la tâche à arrêter ?"
unstart_select = "À quel projet appartient la tâche à arrêter ?"


quit_button = " | (Q)uitter "


def input(prompt):
    var = typer.prompt(prompt + quit_button)
    low = var.lower().strip()
    if low == "q":
        print("OK Bye !")
        sys.exit(0)
    return var.strip()
