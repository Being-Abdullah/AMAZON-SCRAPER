
from pymongo import MongoClient
from bson.objectid import ObjectId
def read_all_documents():
    # Connect to the MongoDB server
    client = MongoClient('xxxxxxxx')

    # Access the database
    db = client['test']

    # Access the collection
    collection = db['products']

    # Read all documents in the collection
    # documents = collection.find({'scrape_status':0}, {'ASIN': 1, '_id': 1}).limit(1000)
    pipeline = [
        { '$match': { 'scrape_status': 0 } },
        { '$sample': { 'size': 50 } },
        { '$project': { 'ASIN': 1, '_id': 1,'product_name':1,'brand':1 ,'commission_payout_aff':1} }
    ]
    documents = list(collection.aggregate(pipeline))
    product_lists = []
    # Print all documents
    for document in documents:
        product_lists.append(document)
    return product_lists
def read_all_documents_variants():
    # Connect to the MongoDB server
    client = MongoClient('xxxxxxxx')

    # Access the database
    db = client['test']

    # Access the collection
    collection = db['variant_products']

    # Read all documents in the collection
    # documents = collection.find({'scrape_status':0}, {'ASIN': 1, '_id': 1}).limit(1000)
    pipeline = [
        { '$match': { 'scrape_status': 0 } },
        { '$sample': { 'size': 50 } },
        { '$project': { 'ASIN': 1, '_id': 1,'product_name':1,'brand':1 ,'commission_payout_aff':1,'final_price_all':1} }
    ]
    documents = list(collection.aggregate(pipeline))
    product_lists = []
    # Print all documents
    for document in documents:
        product_lists.append(document)
    return product_lists

def read_all_documents_nllproduct():
    # Connect to the MongoDB server
    client = MongoClient('xxxxxxxx')

    # Access the database
    db = client['test']

    # Access the collection
    collection = db['null_products']

    # Read all documents in the collection
    # documents = collection.find({'scrape_status':0}, {'ASIN': 1, '_id': 1}).limit(1000)
    pipeline = [
        { '$match': { 'scrape_status': 0 } },
        { '$sample': { 'size': 50 } },
        { '$project': { 'ASIN': 1, '_id': 1 ,'commission_payout_aff':1} }
    ]
    documents = list(collection.aggregate(pipeline))
    product_lists = []
    # Print all documents
    for document in documents:
        product_lists.append(document)
    return product_lists
def check_documents_nllproduct():
    # Connect to the MongoDB server
    client = MongoClient('xxxxxxxx')

    # Access the database
    db = client['test']

    # Access the collection
    collection = db['null_products']

    # Read all documents in the collection
    documents = collection.find_one({'scrape_status':0}, {'ASIN': 1, '_id': 1})
    # pipeline = [
    #     { '$match': { 'scrape_status': 0 } },
    #     { '$sample': { 'size': 5 } },
    #     { '$project': { 'ASIN': 1, '_id': 1 } }
    # ]
    # documents = list(collection.aggregate(pipeline))
    return list(documents)

def check_documents():
    # Connect to the MongoDB server
    client = MongoClient('xxxxxxxx')

    # Access the database
    db = client['test']

    # Access the collection
    collection = db['products']

    # Read all documents in the collection
    documents = collection.find_one({'scrape_status':0}, {'ASIN': 1, '_id': 1,'commission_payout_aff':1})
    # pipeline = [
    #     { '$match': { 'scrape_status': 0 } },
    #     { '$sample': { 'size': 5 } },
    #     { '$project': { 'ASIN': 1, '_id': 1 } }
    # ]
    # documents = list(collection.aggregate(pipeline))
    return list(documents)
def check_documents_variants():
    # Connect to the MongoDB server
    client = MongoClient('xxxxxxxx')

    # Access the database
    db = client['test']

    # Access the collection
    collection = db['variant_products']

    # Read all documents in the collection
    documents = collection.find_one({'scrape_status':0}, {'ASIN': 1, '_id': 1,'commission_payout_aff':1})
    # pipeline = [
    #     { '$match': { 'scrape_status': 0 } },
    #     { '$sample': { 'size': 5 } },
    #     { '$project': { 'ASIN': 1, '_id': 1 } }
    # ]
    # documents = list(collection.aggregate(pipeline))
    return list(documents)

def update_field_by_id(document_id, update_fields,product_found,img_src):
    # Replace the following with your MongoDB connection details
    client = MongoClient("xxxxxxxx")
    db = client["test"]
    collection = db['products']
    destination_collection=db['null_products']
    # Create the filter and update objects
    filter = {"_id": ObjectId(document_id)}
    if img_src is not None:

        update = {"$set": {"deal": update_fields,"image_encoded_string":img_src,'scrape_status':1}}
    else:
       update = {"$set": {"deal": update_fields,'scrape_status':1}}
    # Update the document

    if product_found:
        result = collection.update_one(filter, update)
        if result.modified_count > 0 :
            print(f"Document with ID {document_id} updated successfully.")
        else:
            print(f"No document found with ID {document_id} or no update was made.")

       
    else:
        document = collection.find_one(filter)
        if document:
            check_Asin = destination_collection.find_one({"ASIN": document["ASIN"]})
            if check_Asin:
                # destination_collection.delete_one(check_Asin)
                destination_collection.delete_many({"ASIN": document["ASIN"]})

            # Insert the document into the destination collection
            destination_collection.insert_one(document)
            result3=destination_collection.update_one(filter, {'$set':{'scrape_status':1}})

            # Remove the document from the source collection
            collection.delete_many({"ASIN": document["ASIN"]})

            print(f" 2 Document with ID {document_id} moved to the destination collection.")
        else:
            print(f" 2 3 No document found with ID {document_id}")
    # Close the MongoDB connection
    client.close()

def update_Coupon_by_id(document_id, update_fields):
    client = MongoClient("xxxxxxxx")
    db = client["test"]
    collection = db['products']
    filter = {"_id": ObjectId(document_id)}
    update = {"$set": {"Coupon": update_fields}}
    result = collection.update_one(filter, update)
    if result.modified_count > 0 :
        print(f"Document with ID {document_id} updated successfully.")
    else:
        print(f"No document found with ID {document_id} or no update was made.")
    client.close()

def update_Coupon_by_id_variants(document_id, update_fields):
    client = MongoClient("xxxxxxxx")
    db = client["test"]
    collection = db['variant_products']
    filter = {"_id": ObjectId(document_id)}
    update = {"$set": {"Coupon": update_fields}}
    result = collection.update_one(filter, update)
    if result.modified_count > 0 :
        print(f"Document with ID {document_id} updated successfully.")
    else:
        print(f"No document found with ID {document_id} or no update was made.")
    client.close()

def update_field_by_id_variants(document_id, update_fields,product_found,img_src,final_price_all):
    # Replace the following with your MongoDB connection details
    client = MongoClient("xxxxxxxx")
    db = client["test"]
    collection = db['variant_products']
    destination_collection=db['null_products']
    # Create the filter and update objects
    filter = {"_id": ObjectId(document_id)}
    if img_src is not None:

        update = {"$set": {"deal": update_fields,"image_encoded_string":img_src,'scrape_status':1,'final_price_all':final_price_all}}
    else:
       update = {"$set": {"deal": update_fields,'scrape_status':1,'final_price_all':final_price_all}}
    # Update the document

    if product_found:
        result = collection.update_one(filter, update)
        if result.modified_count > 0 :
            print(f"Document with ID {document_id} updated successfully.")
        else:
            print(f"No document found with ID {document_id} or no update was made.")

        # result2 = collection.update_one(filter, {'$set':{'scrape_status':1}})
        # # result3 = collection.update_one(filter, {'$set':{'scrape_status':1}})

        # if result2.modified_count > 0:
        #     print(f"Document with ID {document_id} updated successfully.")
        # else:
        #     print(f"No document found with ID {document_id} or no update was made.")
    else:
        document = collection.find_one(filter)
        if document:
            check_Asin = destination_collection.find_one({"ASIN": document["ASIN"]})
            if check_Asin:
                # destination_collection.delete_one(check_Asin)
                destination_collection.delete_many({"ASIN": document["ASIN"]})

            # Insert the document into the destination collection
            destination_collection.insert_one(document)
            result3=destination_collection.update_one(filter, {'$set':{'scrape_status':1}})

            # Remove the document from the source collection
            collection.delete_many({"ASIN": document["ASIN"]})

            print(f" 2 Document with ID {document_id} moved to the destination collection.")
        else:
            print(f" 2 3 No document found with ID {document_id}")
    # Close the MongoDB connection
    client.close()

def update_field_by_id_variants_final_price(document_id,final_price_all,parent_category,child_category):
    client = MongoClient("xxxxxxxx")
    db = client["test"]
    collection = db['variant_products']
    filter = {"_id": ObjectId(document_id)}
    update = {"$set": {"final_price_all": final_price_all,'parent_category':parent_category,'child_category':child_category}}
    result = collection.update_one(filter, update)
    if result.modified_count > 0 :
        print(f"Document with ID {document_id} updated successfully.")
    else:
        print(f"No document found with ID {document_id} or no update was made.")
    client.close()


def update_nllproduct_field_by_id(document_id, update_fields,product_found,img_src):
    # Replace the following with your MongoDB connection details
    client = MongoClient("xxxxxxxx")
    db = client["test"]
    collection = db['products']
    destination_collection=db['null_products']
    # Create the filter and update objects
    filter = {"_id": ObjectId(document_id)}
    if img_src is not None:

        update = {"$set": {"deal": update_fields,"image_encoded_string":img_src,'scrape_status':1}}
    else:
       update = {"$set": {"deal": update_fields,'scrape_status':1}}
    # update = {"$set": {"deal": update_fields,"image_encoded_string":img_src}}

    # Update the document

    if product_found:
        document = destination_collection.find_one(filter)
        if document:
            check_Asin = collection.find_one({"ASIN": document["ASIN"]})
            if check_Asin:
                destination_collection.delete_many({"ASIN": document["ASIN"]})
                collection.delete_many({"ASIN": document["ASIN"]})


            collection.insert_one(document)

            result = collection.update_one(filter, update)
            if result.modified_count > 0 :
                print(f"Document with ID {document_id} updated successfully.")
            else:
                print(f"No document found with ID {document_id} or no update was made.")

            result2 = collection.update_one(filter, {'$set':{'scrape_status':1}})
            result3 = collection.update_one(filter, {'$set':{'price':update_fields['price']}})
            # result3 = collection.update_one(filter, {'$set':{'scrape_status':1}})

            if result2.modified_count > 0:
                print(f"Document with ID {document_id} updated successfully.")
                destination_collection.delete_many({"ASIN": document["ASIN"]})

            else:
                print(f"No document found with ID {document_id} or no update was made.")
    else:
        document = destination_collection.find_one(filter)
        if document:
            check_Asin = destination_collection.find_one({"ASIN": document["ASIN"]})
            if check_Asin:
                destination_collection.delete_many({"ASIN": document["ASIN"]})
                destination_collection.insert_one(document)
                result2 = destination_collection.update_one(filter, {'$set':{'scrape_status':1}})


            # result3 = collection.update_one(filter, {'$set':{'scrape_status':1}})

        if result2.modified_count > 0:
            print(f"Document with ID {document_id} updated successfully.")


        else:
            print(f"No document found with ID {document_id} or no update was made.")
    # Close the M