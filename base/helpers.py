import os


def team_foto_file_path(instance, filename: str) -> str:
    _, extension = os.path.splitext(filename)

    file = f"{instance.first_name}_{instance.last_name}.{extension}"

    return os.path.join("uploads/team/", file)


def case_file_path(instance, filename: str) -> str:
    _, extension = os.path.splitext(filename)

    file = f"{instance.name}.{extension}"

    return os.path.join("uploads/case/", file)
