from core.libs.exceptions import FyleError
from core.libs import helpers, assertions
from marshmallow.exceptions import ValidationError
from flask import Blueprint, abort
from core import db
from core.apis import decorators
from core.apis.decorators import Principal
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, GradeEnum

from core.models.assignments import Assignment, AssignmentStateEnum
from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignment(p):
    teacher_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.grade_student(
        _id = grade_assignment_payload.id,
        _grade=grade_assignment_payload.grade,
        principal=p
    )

    db.session.commit()
    graded_assignment=AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(graded_assignment)