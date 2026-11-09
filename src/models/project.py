class Project:

    def __init__(
        self,
        project_id,
        project_name,
        start_date,
        end_date,
        project_status
    ):

        self.project_id = project_id
        self.project_name = project_name
        self.start_date = start_date
        self.end_date = end_date
        self.project_status = project_status

    # Convert project details into a tuple
    def to_tuple(self):

        return (
            self.project_id,
            self.project_name,
            self.start_date,
            self.end_date,
            self.project_status
        )