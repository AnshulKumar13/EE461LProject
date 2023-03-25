from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from database.models import HardwareSet, Projects
from mongoengine import ValidationError, NotUniqueError
from api.routes.validators import parse_error
import json
from datetime import datetime

hardware = Blueprint('hardware', __name__)


@hardware.route('/', methods=['POST'])
@jwt_required()
def hardware_create():
    """POST hardware/
    Desc: Creates a new hardware set
    Returns:
        201: newly created hardware set
        422: validation errors
    """
    req = request.get_json()
    try:
        new_hardware_set = HardwareSet(**req).save()
        return new_hardware_set.to_json(), 201
    except ValidationError as e:
        return parse_error(e), 422
    except NotUniqueError as e:
        return { 'msg': str(e) }, 422


@hardware.route('/', methods=['GET'])
@jwt_required()
def hardware_read():
    """GET hardware/
    Desc: Gets all available hardware sets
    Returns:
        200: all hardware sets in the database
    """
    return HardwareSet.objects.to_json(), 200

@hardware.route('/<id>', methods=['GET'])
@jwt_required()
def hardware_read_id(id):
    """GET hardware/<id>
    Desc: Gets hardware set associated with a project ID
    Returns:
        200: all hardware sets in the database
        404: project not found
        422: validation errors
    """
    try:
        curr_project = Projects.objects(id=id).first()
        if curr_project:
            hardware_list = curr_project["hardware"]
            return json.dumps(hardware_list, default=str), 200
        else:
            return {'msg': 'Project not found'}, 404
    except ValidationError as e:
        return parse_error(e), 422


@hardware.route('/<id>', methods=['PUT'])
@jwt_required()
def hardware_update(id):
    """PUT hardware/<id>
    Desc: Updates a specific hardware set
    Returns:
        200: updated hardware set object
        404: hardware set not found
        422: validation errors
    """
    req = request.get_json()
    try:
        hardware_set = HardwareSet.objects(id=id).first()
        if hardware_set:
            hardware_set.update(**req)
            hardware_set.reload()
            return hardware_set.to_json(), 200
        else:
            return {'msg': 'Hardware set not found'}, 404
    except ValidationError as e:
        return parse_error(e), 422


@hardware.route('/<id>', methods=['DELETE'])
@jwt_required()
def hardware_delete(id):
    """DELETE hardware/<id>
    Desc: Deletes a specific hardware set from the database
    Returns:
        200: success message
        404: hardware set not found
        422: validation errors
    """
    try:
        if HardwareSet.objects(id=id).delete() > 0:
            return {'msg': 'Hardware set successfully deleted'}, 200
        else:
            return {'msg': 'Hardware set not found'}, 404
    except ValidationError as e:
        return parse_error(e), 422


@hardware.route('/check-out/<id>', methods=['POST'])
@jwt_required()
def hardware_checkout(id):
    """POST hardware/check-out/<id>
    Desc: Checks out a quantity of this hardware set for a particular project
    Returns:
        200: updated hardware set
        404: project not found
        422: validation errors
    """
    req = request.get_json()
    try:
        project = Projects.objects(id=req["project_id"]).first()
        if project:
            hardware_set = HardwareSet.objects(id=id).first()
            project_hardware = project.hardware
            found = False
            for hardware in project_hardware:
                if hardware["_id"] == id:
                    found = True
                    hardware["amount"] += req["amount"]
            if not found:
                project_hardware.append({
                    "_id": id,
                    "name": hardware_set["name"],
                    "amount": req["amount"],
                    "cost": 0,
                    "checkout_time": datetime.now()
                })
            # hardware_set.update(dec__available=req["amount"]) -- Can't use this while Mongoengine bug is there
            hardware_set.update(available=hardware_set.available-req["amount"])
            hardware_set.reload()
            project.update(hardware=project_hardware)
            project.reload()
            return hardware_set.to_json(), 200
        else:
            return {'msg': 'Project not found'}, 404
    except ValidationError as e:
        return parse_error(e), 422


@hardware.route('/check-in/<id>', methods=['POST'])
@jwt_required()
def hardware_checkin(id):
    """POST hardware/check-in/<id>
    Desc: Checks in a quantity of this hardware set for a particular project
    Returns:
        200: updated hardware set
        404: project not found or hardware set not found on this project
        422: validation errors
    """
    req = request.get_json()
    try:
        project = Projects.objects(id=req["project_id"]).first()
        if project:
            hardware_set = HardwareSet.objects(id=id).first()
            project_hardware = project.hardware
            found = False
            remove = None
            for hardware in project_hardware:
                if hardware["_id"] == id:
                    found = True
                    hardware["amount"] -= req["amount"]
                    if hardware["amount"] == 0:
                        remove = hardware
            if not found or hardware_set == None:
                return {'msg': 'Hardware Set not found for this project'}, 404
            if remove is not None:
                project_hardware.remove(remove)
            hardware_set.update(inc__available=req["amount"])
            hardware_set.reload()
            project.update(hardware=project_hardware)
            project.reload()
            return hardware_set.to_json(), 200
        else:
            return {'msg': 'Project not found'}, 404
    except ValidationError as e:
        return parse_error(e), 422