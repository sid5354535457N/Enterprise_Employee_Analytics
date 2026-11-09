class Review:

    def __init__(
        self,
        employee_id,
        review_date,
        performance_score,
        performance_rating,
        review_comments,
        review_id=None
    ):

        self.review_id = review_id
        self.employee_id = employee_id
        self.review_date = review_date
        self.performance_score = performance_score
        self.performance_rating = performance_rating
        self.review_comments = review_comments

    # Convert review details into a tuple
    def to_tuple(self):

        return (
            self.employee_id,
            self.review_date,
            self.performance_score,
            self.performance_rating,
            self.review_comments
        )