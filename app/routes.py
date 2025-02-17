from app import db
from flask import request, Blueprint, jsonify
from .models import Customer, Video, Rental
from datetime import datetime


# create Blueprints:
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False



### CRUD for CUSTOMERS  ###

# GET /customers (define a route with default empty string for GET)
@customers_bp.route("", methods=["GET"], strict_slashes=False)
def customers_index():

    sort_query = request.args.get("sort")
    page_number_query = request.args.get("n", type=int)
    query_per_page = request.args.get("p", type=int)

    if sort_query == "name":
        if query_per_page is int and page_number_query is int:
            customers = Customer.query.paginate(page=query_per_page, per_page=page_number_query)   # need to combine with the sort_query here
        else:
            customers = Customer.query.order_by("name")

    elif query_per_page is int and page_number_query is int:
        customers = Customer.query.paginate(page=query_per_page, per_page=page_number_query)
    else: 
        customers = Customer.query.order_by("id") 

    customers_response = [customer.to_dict() for customer in customers]

    return jsonify(customers_response), 200  


# GET /customers/<id> (define a new route to GET a specific customer)
@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_one_customer(customer_id):

    if not is_int(customer_id):        
        return {"message": f"ID {customer_id} must be an integer"}, 400
    
    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(None), 404
    else:
        customer_dict = customer.to_dict()
     
    return jsonify(customer_dict), 200


# POST /customers (define a route with default empty string for POST)
@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():  

    request_body = request.get_json()
    name = request_body.get("name")
    postal_code = request_body.get("postal_code")
    phone = request_body.get("phone")

    if not name or not postal_code or not phone:
        return jsonify({"details": "Invalid data"}), 400 
    
    # create new customer entry:
    new_customer = Customer(
        name = name, 
        postal_code = postal_code, 
        phone = phone, 
        registered_at = datetime.now()
    )

    db.session.add(new_customer)   
    db.session.commit()    

    customer_dict = new_customer.to_dict()

    return jsonify(customer_dict), 201


# PUT /customers/<id> (define a new route to update (PUT) one customer by its id):
@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_single_customer(customer_id):

    if not is_int(customer_id):        
        return {"message": f"ID {customer_id} must be an integer"}, 400
    
    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(None), 404

    request_body = request.get_json()
    name = request_body.get("name")
    postal_code = request_body.get("postal_code")
    phone = request_body.get("phone")

    if not name or not postal_code or not phone:
        return jsonify({"details": "Invalid data"}), 400 

    customer.name = name
    customer.postal_code = postal_code
    customer.phone = phone

    db.session.commit()

    customer_dict = customer.to_dict()
    
    return jsonify(customer_dict), 200


# DELETE /customers/<id> (define a new route to DELETE one task by its id):
@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_customer(customer_id):

    if not is_int(customer_id):        
        return {"message": f"ID {customer_id} must be an integer"}, 400

    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(None), 404
   
    db.session.delete(customer)
    db.session.commit()

    return jsonify({"details": f'Customer {customer.id} "{customer.name}" successfully deleted', "id": customer.id}), 200



### CRUD for VIDEOS ###

# GET /videos
@videos_bp.route("", methods=["GET"], strict_slashes=False)
def videos_index():
    videos = Video.query.all() 

    videos_response = [video.to_dict() for video in videos]

    return jsonify(videos_response), 200 


# GET /videos/<id>
@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_one_video(video_id):

    if not is_int(video_id):        
        return {"message": f"ID {video_id} must be an integer"}, 400
    
    video = Video.query.get(video_id)

    if video is None:
        return jsonify(None), 404
    else:
        video_dict = video.to_dict()
     
    return jsonify(video_dict), 200


# POST /videos
@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_video():  

    request_body = request.get_json()
    title = request_body.get("title")
    release_date = request_body.get("release_date")
    total_inventory = request_body.get("total_inventory")

    if not title or not release_date or not total_inventory:
        return jsonify({"details": "Invalid data"}), 400 
    
    # create new video entry:
    new_video = Video(
        title = title, 
        release_date = release_date, 
        total_inventory = total_inventory, 
        available_inventory = total_inventory
    )

    db.session.add(new_video)   
    db.session.commit()     

    video_dict = new_video.to_dict()

    return jsonify(video_dict), 201


# PUT /videos/<id>
@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_single_video(video_id):

    if not is_int(video_id):        
        return {"message": f"ID {video_id} must be an integer"}, 400
    
    video = Video.query.get(video_id)

    if video is None:
        return jsonify(None), 404

    request_body=request.get_json()
    title = request_body.get("title")
    release_date = request_body.get("release_date")
    total_inventory = request_body.get("total_inventory")

    if not title or not release_date or not total_inventory:
        return jsonify({"details": "Invalid data"}), 400 

    video.title = title
    video.release_date = release_date
    video.total_inventory = total_inventory

    db.session.commit()

    video_dict = video.to_dict()
    
    return jsonify(video_dict), 200


# DELETE /videos/<id>
@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_video(video_id):

    if not is_int(video_id):        
        return {"message": f"ID {video_id} must be an integer"}, 400

    video = Video.query.get(video_id)

    if video is None:
        return jsonify(None), 404
   
    db.session.delete(video)
    db.session.commit()

    video_dict = video.to_dict()

    return jsonify(video_dict), 200



### CRUD for RENTALS ###

# POST /rentals/check-out
@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def create_rental():  
    # Customer rents out a specific video, then a rental is created (id and due date)
    request_body = request.get_json()
    customer_id = request_body.get("customer_id")
    video_id = request_body.get("video_id")

    if not is_int(customer_id) or not is_int(video_id):        
        return {"message": f"Please input an integer"}, 400

    # if request body is missing customer or video field:
    if not customer_id or not video_id:
        return jsonify({"details": "Invalid data"}), 400 
    
    # if customer or video does not exist:
    if customer_id is None or video_id is None:
        return jsonify(None), 404

    # get both customer_id and video_id:
    video = Video.query.get(video_id)

    # If inventory check-out empty:
    if video.available_inventory == 0:
        return jsonify({"details": "Invalid data"}), 400 

    # separating the business: 
    new_rental = Rental.checkout(customer_id, video_id)
    rental_dict = new_rental.to_dict()
    return jsonify(rental_dict), 200


# POST /rentals/check-in (customer (with customer_id) returns a specific video (with video_id))
@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def return_rental():
    request_body = request.get_json()
    customer_id = request_body.get("customer_id")
    video_id = request_body.get("video_id")

    if not is_int(customer_id):        
        return {"message": f"Please input an integer"}, 400

    # if request body is missing customer or video field:
    if not customer_id or not video_id:
        return jsonify({"details": "Invalid data"}), 400 
    
    # if customer or video does not exist:
    if customer_id is None or video_id is None:
        return jsonify(None), 404
    
    # get both customer_id and video_id
    customer = Customer.query.get(customer_id)  
    video = Video.query.get(video_id)

    for rental in customer.customers:
        if rental.video_id == video_id and rental.checked_out == True:
            video.available_inventory += 1
            customer.videos_checked_out_count -= 1
            rental.checked_out = False
        else:
            return jsonify(None), 400

    db.session.commit()  

    return_dict = {
        "customer_id": customer_id,
        "video_id": video_id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }
    
    return jsonify(return_dict), 200 


# GET /customers/<id>/rentals (lists videos a customer currently has checked-out)
@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def videos_rented_by_one_customer(customer_id):

    if not is_int(customer_id):        
        return {"message": f"ID {customer_id} must be an integer"}, 400

    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(None), 404

    # Get all rentals associated with a customer at id customer_id
    all_rentals_for_customer = db.session.query(Rental).join(Customer, Customer.id==Rental.customer_id)\
            .join(Video, Video.id==Rental.video_id).filter(Customer.id == customer_id).all()
    
    all_customer_videos = []
    for rental in all_rentals_for_customer:
        video = Video.query.get(rental.video_id)
        all_customer_videos.append({
            "title": video.title,
            "release_date": video.release_date,
            "due_date": rental.due_date 
        })
   
    return jsonify(all_customer_videos), 200


# GET /videos/<id>/rentals (lists customers who currently have the video checked-out)
@videos_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
def customers_rented_one_video(video_id):

    if not is_int(video_id):        
        return {"message": f"ID {video_id} must be an integer"}, 400

    video = Video.query.get(video_id)

    if video is None:
        return jsonify(None), 404
    
    # Get all rentals associated with a video at id video_id
    all_rentals_for_video = db.session.query(Rental).join(Video, Video.id==Rental.video_id)\
        .join(Customer, Customer.id==Rental.customer_id).filter(Video.id==video_id).all()


    all_video_customers = []
    for rental in all_rentals_for_video:
        customer = Customer.query.get(rental.customer_id)        # also try rental.customer 

        all_video_customers.append({
            "name": customer.name,
            "postal_code": customer.postal_code,
            "phone": customer.phone,
            "due_date": rental.due_date 
        })

    return jsonify(all_video_customers), 200





