from dataclasses import dataclass
from lefaire.connect import connect


@dataclass
class Project:
    ID: int
    name: str
    created: str
    started: str
    completed: str
    dueDate: str
    description: str


@dataclass
class Task:
    ID: int
    projectID: int
    rank: int
    body: str
    created: str
    started: str
    completed: str


# Retrieve all projects
def get_projects():
    conn = connect()
    cur = conn.cursor()
    projects = []
    cur.execute(
        "SELECT ID, Name, Created, Started, CompletionDate, DueDate, Description from Project"
    )

    for (
        ID,
        name,
        created,
        started,
        completed,
        dueDate,
        description,
    ) in cur:
        project = Project(ID, name, created, started, completed, dueDate, description)
        projects.append(project)

    conn.close()
    return projects


# Retrieve on particular project
def get_single_project(projectID):

    conn = connect()
    cur = conn.cursor()

    if not projectIDExists(cur, projectID):
        raise Exception("Projet introuvable")
    project = None
    cur.execute(
        "SELECT Name, Created, Started, CompletionDate, DueDate, Description from Project WHERE ID = ?",
        (projectID,),
    )
    for (
        name,
        created,
        started,
        completed,
        dueDate,
        description,
    ) in cur:
        project = Project(
            projectID,
            name,
            created,
            started,
            completed,
            dueDate,
            description,
        )

    conn.close()
    return project


# Show all tasks for a project
def get_tasks(projectID: int):

    conn = connect()
    cur = conn.cursor()

    if not (projectIDExists(cur, projectID)):
        raise Exception("Projet introuvable")
    tasks = []
    cur.execute(
        "SELECT ID, Rank, Body, Created, Started, CompletionDate FROM Task WHERE ProjectID = ? ORDER BY Rank;",
        (projectID,),
    )

    for ID, rank, body, created, started, completed in cur:
        task = Task(ID, projectID, rank, body, created, started, completed)
        tasks.append(task)

    tasks = clean_ranks(cur, tasks)
    conn.commit()
    conn.close()
    return tasks


def clean_ranks(cur, tasksList):

    # split todo and done()
    todo = []
    done = []
    for task in tasksList:
        if task.completed:
            done.append(task)
        else:
            todo.append(task)
    newList = done + todo
    newOrder(cur, newList)
    return newList


# get a specific task from a project
def get_single_task(projectID, rank):

    get_single_project(projectID)

    conn = connect()
    cur = conn.cursor()

    if not taskRankExists(cur, projectID, rank):
        raise NameError("Tâche introuvable")

    cur.execute(
        "SELECT ID, Body, Created, Started, CompletionDate FROM Task WHERE ProjectID = ? AND Rank = ?;",
        (projectID, rank),
    )
    for ID, body, created, started, completed in cur:
        task = Task(ID, projectID, rank, body, created, started, completed)

    conn.close()
    return task


def get_task_ID(projectID, rank):
    conn = connect()
    cur = conn.cursor()

    if not taskRankExists(cur, projectID, rank):
        raise NameError("Tâche introuvable")

    cur.execute(
        "SELECT ID FROM Task WHERE ProjectID = ? AND Rank = ?;",
        (projectID, rank),
    )
    id = cur.fetchone()[0]
    conn.close()
    return id


def get_task_by_ID(taskID):

    conn = connect()
    cur = conn.cursor()

    task = None
    cur.execute(
        "SELECT ProjectID, Rank, Body, Created, Started, CompletionDate FROM Task WHERE ID = ?;",
        (taskID,),
    )
    for projectID, rank, body, created, started, completed in cur:
        task = Task(taskID, projectID, rank, body, created, started, completed)
    conn.close()
    return task


def projectNameExists(cur, projectName: str):
    cur.execute(
        "SELECT EXISTS (SELECT * FROM Project WHERE Name = ?) ;",
        (projectName,),
    )
    bool = cur.fetchone()[0]
    return bool


def projectIDExists(cur, projectID: int):
    cur.execute(
        "SELECT EXISTS (SELECT * FROM Project WHERE ID = ?) ;",
        (projectID,),
    )
    bool = cur.fetchone()[0]
    return bool


def toID(input: str):

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT ID FROM Project WHERE Name = ?;", (input,))
    res = cur.fetchone()
    conn.close()
    if res is not None:
        id = res[0]
        return id
    else:
        try:
            return int(input)
        except Exception:
            raise Exception(f"'{input}' est introuvable")
            pass


# Add a project
def create_project(projectName="Nouveau Projet", description=None):

    conn = connect()
    cur = conn.cursor()

    projectName = projectName.strip()
    if description:
        description = description.strip()
    if projectNameExists(cur, projectName):
        raise NameError("Le projet existe déjà !")

    if not description:
        description = None

    cur.execute(
        "INSERT INTO Project (Name, Created, Description) VALUES ( ?, CURRENT_TIMESTAMP, ?);",
        (projectName, description),
    )

    conn.commit()
    conn.close()


def update_rank(cur, ID, newRank):
    cur.execute("UPDATE Task SET Rank = ? WHERE ID = ?;", (newRank, ID))


def newOrder(cur, list):

    for i in range(len(list)):
        task = list[i]
        update_rank(cur, task.ID, i + 1)


def taskBodyExists(cur, projectID, body):
    cur.execute(
        "SELECT EXISTS (SELECT * FROM Task WHERE ProjectID = ? AND Body = ?);",
        (projectID, body),
    )
    bool = cur.fetchone()[0]
    return bool


def taskRankExists(cur, projectID, rank):
    cur.execute(
        "SELECT EXISTS (SELECT * FROM Task WHERE ProjectID = ? AND Rank = ?);",
        (projectID, rank),
    )
    bool = cur.fetchone()[0]
    return bool


# Add a task to a project
def add_task(projectID: int, body: str):

    project = get_single_project(projectID)

    conn = connect()
    cur = conn.cursor()

    if taskBodyExists(cur, projectID, body):
        raise Exception("La tâche existe déjà")

    body = body.strip()
    tasksList = get_tasks(projectID)
    rank = len(tasksList) + 1
    cur.execute(
        "INSERT INTO Task (ProjectID, Rank, Body) VALUES (?, ?, ?);",
        (projectID, rank, body),
    )

    conn.commit()
    conn.close()

    if project.completed:
        uncomplete_project(projectID)


# Update project
def rename_project(projectID, newName):

    get_single_project(projectID)

    conn = connect()
    cur = conn.cursor()

    newName = newName.strip()
    cur.execute("UPDATE Project SET Name = ? WHERE ID = ?", (newName, projectID))

    conn.commit()
    conn.close()


def update_description(projectID, newDescription):

    get_single_project(projectID)

    conn = connect()
    cur = conn.cursor()

    newDescription = newDescription.strip()
    cur.execute(
        "UPDATE Project SET Description = ? WHERE ID = ?", (newDescription, projectID)
    )
    conn.commit()
    conn.close()


def update_due_date(projectID, dueDate):

    get_single_project(projectID)

    conn = connect()
    cur = conn.cursor()

    cur.execute("UPDATE Project SET DueDate = ? WHERE ID = ?", (dueDate, projectID))
    conn.commit()
    conn.close()


def start_project(projectID):

    get_single_project(projectID)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE Project SET Started = CURRENT_TIMESTAMP WHERE ID = ?", (projectID,)
    )
    conn.commit()
    conn.close()


def unstart_project(projectID):

    get_single_project(projectID)

    conn = connect()
    cur = conn.cursor()

    cur.execute("UPDATE Project SET Started = NULL WHERE ID = ?", (projectID,))
    conn.commit()
    conn.close()


def complete_project(projectID):

    get_single_project(projectID)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE Project SET CompletionDate = CURRENT_TIMESTAMP  WHERE ID = ?",
        (projectID,),
    )
    conn.commit()
    conn.close()


def uncomplete_project(projectID):

    get_single_project(projectID)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE Project SET CompletionDate = NULL WHERE ID = ?",
        (projectID,),
    )
    conn.commit()
    conn.close()


def relocate_project(projectID, newID):

    get_single_project(projectID)

    conn = connect()
    cur = conn.cursor()

    if projectIDExists(cur, newID):
        raise Exception(f"Le projet n°{newID} existe déjà !")

    cur.execute(
        "UPDATE Project SET ID = ? WHERE ID = ?",
        (
            newID,
            projectID,
        ),
    )
    # changer le project ID de ces taches
    cur.execute(
        "UPDATE Task SET ProjectID = ? WHERE ProjectID = ?",
        (
            newID,
            projectID,
        ),
    )

    conn.commit()
    conn.close()
    change_auto_increment()


def change_auto_increment():

    conn = connect()
    cur = conn.cursor()

    try:
        # find the bigger ID
        cur.execute("SELECT MAX(ID) FROM Project")
        maxID = cur.fetchone()[0]
        # Make the auto-increment the next number
        if maxID:
            auto_increment = f"{maxID + 1}"
            cur.execute(f"ALTER TABLE Project AUTO_INCREMENT={auto_increment};")
            cur.execute("COMMIT")
    except Exception:
        raise Exception("Erreur de manipulation des auto-increments ")
    finally:
        conn.commit()
        conn.close()


# Update a task
def update_body(projectID, rank, newBody):

    get_single_task(projectID, rank)

    conn = connect()
    cur = conn.cursor()

    newBody = newBody.strip()
    cur.execute(
        "UPDATE Task SET Body = ? WHERE ProjectID = ? AND Rank = ?",
        (newBody, projectID, rank),
    )
    conn.commit()
    conn.close()


def swap_rank(projectID, currentRank, newRank):
    firstTask = get_single_task(projectID, currentRank)
    secondTask = get_single_task(projectID, newRank)
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE Task SET Rank = ? WHERE ID=?", (newRank, firstTask.ID))
    cur.execute("UPDATE Task SET Rank = ? WHERE ID=?", (currentRank, secondTask.ID))
    conn.commit()
    conn.close()


def move_up(projectID, rank):
    task = get_single_task(projectID, rank)
    if rank == 1:
        raise Exception(
            f"'{task.body}' est la première tâche, elle ne peut donc pas monter plus haut."
        )
    swap_rank(projectID, rank, rank - 1)


def move_down(projectID, rank):

    task = get_single_task(projectID, rank)
    try:
        get_single_task(projectID, rank + 1)
    except Exception:
        raise Exception(
            f"'{task.body}' est la dernière tâche, elle ne peut donc pas descendre plus bas."
        )
    swap_rank(projectID, rank, rank + 1)


def move_ext(projectID, rank, ext):

    task = get_single_task(projectID, rank)
    ext = ext.lower()
    tasksList = get_tasks(projectID)

    conn = connect()
    cur = conn.cursor()
    # split todo and done
    todo = []
    done = []
    if rank == 1 and ext == "top":
        raise Exception(
            f"'{task.body}' est déjà la première tâche, elle ne peut donc pas monter plus haut."
        )
    if rank == len(tasksList) and ext == "bottom":
        raise Exception(
            f"'{task.body}' est déjà la dernière tâche, elle ne peut donc pas descendre plus bas."
        )
    for current in tasksList:
        if current != task:
            if current.completed:
                done.append(current)
            else:
                todo.append(current)
    if ext == "top":
        if task.completed:
            done.insert(0, task)
        else:
            todo.insert(0, task)
    else:
        if task.completed:
            done.append(task)
        else:
            todo.append(task)

    newList = done + todo
    newOrder(cur, newList)
    conn.commit()
    conn.close()


def move(projectID, rank, dir):

    dir = dir.lower()
    if dir == "up":
        move_up(projectID, rank)
    elif dir == "down":
        move_down(projectID, rank)
    elif dir == "top" or dir == "bottom":
        move_ext(projectID, rank, dir)
    else:
        raise Exception("La direction ne peut être que 'top', 'bottom', 'up' ou 'down'")


def start_task(projectID, rank):

    task = get_single_task(projectID, rank)

    conn = connect()
    cur = conn.cursor()

    if task.started:
        raise Exception(f"La tâche '{task.body}' est déjà commencée.")
    if task.completed:
        raise Exception(f"La tâche '{task.body}' est déjà terminée.")
    cur.execute(
        "UPDATE Task SET started = CURRENT_TIMESTAMP WHERE ProjectID = ? AND Rank = ?",
        (projectID, rank),
    )
    conn.commit()
    conn.close()
    project = get_single_project(projectID)
    if not project.started:
        start_project(projectID)
    if task.completed:
        uncomplete_task(projectID, rank)


def noTasksStarted(tasksList):
    for task in tasksList:
        if task.started or task.completed:
            return False
    return True


def checkifStarted(cur, projectID):
    tasksList = get_tasks(projectID)
    if noTasksStarted(tasksList):
        unstart_project(projectID)


def unstart_task(projectID, rank):

    task = get_single_task(projectID, rank)
    conn = connect()
    cur = conn.cursor()

    if not task.started:
        raise Exception(f"La tâche '{task.body}' n'est pas encore commencée.")
    if task.completed:
        raise Exception(f"La tâche '{task.body}' est déjà terminée.")
    cur.execute(
        "UPDATE Task SET started = NULL WHERE ProjectID = ? AND Rank = ?",
        (projectID, rank),
    )
    conn.commit()
    conn.close()
    project = get_single_project(projectID)
    if project.started:
        checkifStarted(cur, projectID)
    updatedTask = get_single_task(projectID, rank)
    if updatedTask.completed:
        uncomplete_task(projectID, rank)


def allTasksComplete(tasksList):
    for task in tasksList:
        if not task.completed:
            return False
    return True


def checkCompleteness(cur, projectID):
    tasksList = get_tasks(projectID)
    if not tasksList:
        uncomplete_project(projectID)
        unstart_project(projectID)
    elif allTasksComplete(tasksList):
        complete_project(projectID)
    else:
        uncomplete_project(projectID)


def complete_task(projectID, rank):

    task = get_single_task(projectID, rank)

    if task.completed:
        raise Exception(f"La tâche '{task.body}' est déjà terminée")

    if int(rank) > 1:
        move_ext(projectID, rank, "top")
    newTask = get_task_by_ID(task.ID)
    rank = newTask.rank
    conn = connect()
    cur = conn.cursor()
    if not task.started:
        start_task(projectID, rank)
    cur.execute(
        "UPDATE Task SET CompletionDate = CURRENT_TIMESTAMP  WHERE ID = ? ",
        (task.ID,),
    )
    conn.commit()
    conn.close()
    checkCompleteness(cur, projectID)
    get_tasks(projectID)


def uncomplete_task(projectID, rank):

    task = get_single_task(projectID, rank)

    conn = connect()
    cur = conn.cursor()

    if not task.completed:
        raise Exception(f"La tâche '{task.body}' n'est pas terminée")
    cur.execute(
        "UPDATE Task SET CompletionDate = NULL WHERE ProjectID = ? AND Rank = ?",
        (projectID, rank),
    )
    conn.commit()
    conn.close()
    checkCompleteness(cur, projectID)


def delete_project(projectID):

    conn = connect()
    cur = conn.cursor()

    if not projectIDExists(cur, projectID):
        raise Exception("Le project n'existe pas ")
    cur.execute("DELETE FROM Project WHERE ID = ?", (projectID,))
    cur.execute("DELETE FROM Task WHERE ProjectID = ?;", (projectID,))
    conn.commit()
    conn.close()
    change_auto_increment()


def delete_task(taskID):
    task = get_task_by_ID(taskID)

    conn = connect()
    cur = conn.cursor()

    projectID = task.projectID
    cur.execute("DELETE FROM Task WHERE ID = ?;", (taskID,))
    conn.commit()
    conn.close()
    checkifStarted(cur, projectID)
    checkCompleteness(cur, projectID)
