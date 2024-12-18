import typer
import os
import lefaire.view as view
import lefaire.data as data
import lefaire.prompt as prompt
from lefaire.connect import setup

from .prompt import input
from typing_extensions import Annotated

app = typer.Typer()
move_app = typer.Typer()
app.add_typer(move_app, name="move", help="Déplacer une tâche dans la liste de tâche.")


@app.command()
def add(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    body: Annotated[str, typer.Argument(help="Corps de la tâche")] = "",
    top: Annotated[
        bool,
        typer.Option(
            "-t",
            "--top",
            help="Mettre la tâche tout en haut ?",
        ),
    ] = False,
):
    """
    Ajouter une tâche.
    """

    try:
        if not select:
            list()
            select = input(prompt.add_select)

        projectID = data.toID(select)

        if not body:
            list(projectID)
            body = input(prompt.task_body)

        project = data.get_single_project(projectID)
        data.add_task(projectID, body)
        taskList = data.get_tasks(projectID)
        task = taskList[-1]

        if top:
            data.move_ext(projectID, task.rank, "top")
            task = data.get_task_by_ID(task.ID)

        list(projectID)
        view.add(task, project)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def create(
    name: Annotated[str, typer.Argument(help="Nom du projet")] = "",
    description: Annotated[str, typer.Argument(help="Description du projet")] = "",
):
    """
    Créer un projet.
    """
    try:
        if not name:
            name = input(prompt.create_name)

        data.create_project(name, description)
        project = data.get_projects()[-1]
        list()
        view.create(project)

    except NameError as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def delete(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    rank: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
    all: Annotated[bool, typer.Option("-a", "--all", "-p", "--project")] = False,
):
    """
    Supprimer un projet. Pour supprimer une tâche, ajouter son rang
    """
    confirm = False
    try:
        if not select:
            if not all:
                all = typer.confirm(view.delete_all_prompt())
                confirm = True
            if all:
                select = input(prompt.delete_select_all)
            else:
                select = input(prompt.delete_select)

        projectID = data.toID(select)

        project = data.get_single_project(projectID)
        if not rank:
            if not all and not confirm:
                confirm = typer.confirm(view.delete_all_prompt())
                all = confirm
            if all:
                delete_project(project)
            else:
                list(project.ID)
                rank = typer.prompt("Quelle tâche doit être supprimée ? ")
        if rank:
            task = data.get_single_task(project.ID, rank)

            delete_task(project, task)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


def delete_project(project):

    confirm = typer.confirm(view.delete_project_warning(project))
    if confirm:
        data.delete_project(project.ID)
        list()
        view.delete_project(project)
    else:
        list()
        view.delete_project_safe(project)


def delete_task(project, task):

    confirm = typer.confirm(view.delete_task_warning(task, project))
    if confirm:
        data.delete_task(task.ID)
        list(project.ID)
        view.delete_task(task, project)
    else:
        list(project.ID)
        view.delete_task_safe(task, project)


@app.command()
def desc(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    description: Annotated[str, typer.Argument(help="Description du projet")] = "",
):
    """
    Ajouter ou modifier la description d'un projet.
    """

    try:
        if not select:
            list()
            select = input(prompt.modify_select)

        projectID = data.toID(select)

        if not description:
            list(projectID)
            description = input(prompt.description)

        data.update_description(projectID, description)
        project = data.get_single_project(projectID)
        list(projectID)
        view.desc(project)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def done(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    rank: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
    commit: Annotated[bool, typer.Option("-g", "-c", "--git", "--commit")] = False,
):
    """
    Marquer une tâche comme terminée.
    """
    try:
        if not select:
            list()
            select = input(prompt.done_select)

        projectID = data.toID(select)

        if not rank:
            list(projectID)
            rank = input(prompt.done_rank)

        project = data.get_single_project(projectID)
        task = data.get_single_task(projectID, rank)

        data.complete_task(projectID, rank)
        task = data.get_task_by_ID(task.ID)
        list(projectID, task.rank)
        view.complete(task, project)

        # run git command if wanted
        cmd = view.commit_cmd(task)
        if commit:
            sure = True
        else:
            sure = typer.confirm(view.commit_prompt(cmd))
        if sure:
            os.system(cmd)
            list(projectID)
            view.commit_success()

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def due(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    date: Annotated[str, typer.Argument(help="Date butoir du projet")] = "",
):
    """
    Ajouter ou modifier une date butoir (JJ/MM/AAA HH:MM:SS).
    """

    try:
        if not select:
            list()
            select = input(prompt.modify_select)

        projectID = data.toID(select)

        if not date:
            list(projectID)
            date = input(prompt.due_date)

        date = view.toUSDate(date)
        data.get_single_project(projectID)
        data.update_due_date(projectID, date)
        project = data.get_single_project(projectID)
        list(projectID)
        view.due(project)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def edit(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    rank: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
    body: Annotated[str, typer.Argument(help="Corps de la tâche")] = "",
):
    """
    Modifier le corps d'une tâche.
    """
    try:
        if not select:
            list()
            select = input(prompt.modify_task_select)

        projectID = data.toID(select)

        if not rank:
            list(projectID)
            rank = input(prompt.modify_rank)
            rank = int(rank)

        if not body:
            list(projectID, rank)
            body = input(prompt.task_body)

        project = data.get_single_project(projectID)
        data.update_body(projectID, rank, body)
        task = data.get_single_task(projectID, rank)
        list(projectID, rank)
        view.edit(task, project)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


def list(select: int = 0, rank: int = 0, long: bool = False):
    """
    Lister les projets et leurs tâches.
    """
    if rank:
        task = data.get_single_task(select, rank)
        view.task_info(task)

    elif select:
        projectID = data.toID(select)
        project = data.get_single_project(projectID)
        taskList = data.get_tasks(projectID)
        view.project_info(project, taskList, long)

    else:
        projectsList = data.get_projects()
        view.list(projectsList)


def project_menu(select):
    choice = typer.prompt(
        "(A)jouter une tâche | (I)nfo d'une tâche | (R)enommer | Changer la (D)escription | Changer la date (B)utoir | (S)upprimer | (Q)uitter "
    )

    choice = choice.lower().strip()
    if choice == "a":
        add(select)
    elif choice == "i":
        rank = typer.prompt("Quel est le rang de la tâche à consulter ? ")
        info(select, rank)
    elif choice == "r":
        rename(select)
    elif choice == "d":
        desc(select)
    elif choice == "b":
        due(select)
    elif choice == "s":
        delete(select, "", True)
    elif choice == "q":
        print("\n")
    else:
        try:

            int(choice)
            data.get_single_task(select, choice)
        except Exception as e:
            pass
            view.error(e)
        else:
            info(select, choice)


def task_menu(select, rank):
    rank = int(rank)
    task = data.get_single_task(select, rank)
    menu = "(E)diter | "
    if not task.started:
        menu += "(C)ommencer | "
    if task.started and not task.completed:
        menu += "(A)rrêter | "
    if not task.completed:
        menu += "(T)erminer | "
    if task.completed:
        menu += "(R)etravailler | "
    menu += "(D)éplacer | (S)upprimer | (Q)uitter "

    choice = typer.prompt(menu)
    choice = choice.lower().strip()
    if choice == "e":
        edit(select, rank)
    if choice == "c":
        start(select, rank)
    if choice == "a":
        unstart(select, rank)
    if choice == "t":
        done(select, rank)
    if choice == "r":
        undo(select, rank)
    if choice == "s":
        delete(select, rank)
    if choice == "q":
        info(select)
    if choice == "d":
        dir = typer.prompt(
            "Déplacer vers le (H)aut | Déplacer vers le (B)as | Mettre en (P)remier | Mettre en (D)ernier "
        )
        dir = dir.lower().strip()
        if dir == "h":
            dir = "up"
        if dir == "b":
            dir = "down"
        if dir == "p":
            dir = "top"
        if dir == "d":
            dir = "bottom"
        move(dir, select, rank)


@app.command()
def info(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    rank: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
    long: Annotated[
        bool,
        typer.Option(
            "-l", "-v", "--long", "--verbose", help="Affiche toutes les tâches ?"
        ),
    ] = False,
):
    """
    Détailler les infos sur un projet.
    """

    try:
        if rank:
            list(select, rank)
            task_menu(select, rank)
        else:
            if not select:
                list()
                select = input(prompt.info_select)

            if select.lower() == "c":
                create()

            else:
                projectID = data.toID(select)
                list(projectID, 0, long)
                project_menu(projectID)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def init():
    """
    Créé un mot de passe et un utilisateur pour se connecter à MariaDB
    """
    try:
        setup()

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def relocate(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    new: Annotated[int, typer.Argument(help="Nouveau Numéro ou nom du projet")] = 0,
):
    """
    Changer le Numéro ou nom d'identifiant d'un projet
    """

    try:
        if not select:
            list()
            select = input(prompt.relocate_select)
        projectID = data.toID(select)

        project = data.get_single_project(projectID)

        if not new:
            custom_prompt = prompt.relocate_new + project.name + " ?"
            new = input(custom_prompt)

        data.relocate_project(projectID, new)
        project = data.get_single_project(projectID)
        list()
        view.relocate(project)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def rename(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    name: Annotated[str, typer.Argument(help="Nouveau nom du projet")] = "",
):
    """
    Renommer un projet.
    """
    try:
        if not select:
            list()
            select = input(prompt.rename_select)

        projectID = data.toID(select)

        if not name:
            name = input(prompt.rename_name)

        data.rename_project(projectID, name)
        list()
        view.rename(projectID, name)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def start(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    rank: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Marquer une tâche comme commencée.
    """
    try:
        if not select:
            list()
            select = input(prompt.start_select)

        projectID = data.toID(select)

        if not rank:
            list(projectID)
            rank = input(prompt.start_rank)

        project = data.get_single_project(projectID)
        data.start_task(projectID, rank)
        task = data.get_single_task(projectID, rank)
        list(projectID)
        view.start(task, project)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def undo(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    rank: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Marquer une tâche comme non terminée.
    """

    try:
        if not select:
            list()
            select = input(prompt.undo_select)

        projectID = data.toID(select)

        if not rank:
            list(projectID)
            rank = input(prompt.undo_rank)

        project = data.get_single_project(projectID)
        task = data.get_single_task(projectID, rank)
        data.uncomplete_task(projectID, rank)
        task = data.get_task_by_ID(task.ID)
        list(projectID)
        view.uncomplete(task, project)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def unstart(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    rank: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Marquer une tâche comme non commencée.
    """

    try:
        if not select:
            list()
            select = input(prompt.unstart_select)

        projectID = data.toID(select)

        if not rank:
            list(projectID)
            rank = input(prompt.unstart_rank)

        project = data.get_single_project(projectID)
        data.unstart_task(projectID, rank)
        task = data.get_single_task(projectID, rank)
        list(projectID)
        view.unstart(task, project)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


def move(
    dir: Annotated[str, typer.Argument(help="Direction")],
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    rank: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche dans la liste de tâche.
    """
    try:
        if not select:
            list()
            select = input(prompt.move_select)

        projectID = data.toID(select)

        if not rank:
            list(projectID)
            rank = input(prompt.move_rank)

        rank = int(rank)
        task = data.get_single_task(projectID, rank)
        data.move(projectID, rank, dir)
        project = data.get_single_project(projectID)
        list(projectID)
        view.move(task, project, dir)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@move_app.command("up")
def move_up(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    rank: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche vers le haut dans la liste de tâche.
    """
    move("up", select, rank)


@move_app.command("down")
def move_down(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    rank: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche vers le bas dans la liste de tâche
    """
    move("down", select, rank)


@move_app.command("top")
def move_top(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    rank: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche tout en haut de la liste de tâche.
    """
    move("top", select, rank)


@move_app.command("bottom")
def move_bottom(
    select: Annotated[str, typer.Argument(help="Numéro ou nom du projet")] = "",
    rank: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche tout en vas de la liste de tâche.
    """
    move("bottom", select, rank)


if __name__ == "__main__":
    app()
