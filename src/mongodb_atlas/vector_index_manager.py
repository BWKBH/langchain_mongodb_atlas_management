from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel
import time
import os

class VectorIndexManager:
	# Create your index model, then create the search index

	def __init__(self
		, db_name: str
		, collection_name: str
		, uri_name:str):
		self.uri = os.getenv(uri_name)
		self.client = MongoClient(self.uri)
		self.collection = self.client[db_name][collection_name]

	def create_hnsw_index(self
		, index_name: str
		, dimensions: int
		, attribute_name: str
		, similarity: str
		, filter_attribute_names: list):
		
		fields = [
			{
				"type": 'vector',
				"path": attribute_name,
				"numDimensions": dimensions,
				"similarity": similarity
			}
		]

		# Add all provided filter fields
		for filter_attribute_name in filter_attribute_names:
			fields.append({
				"type": "filter",
				"path": filter_attribute_name
			})

		# Construct the SearchIndexModel
		search_index_model = SearchIndexModel(
			definition={
				"fields": fields
			},
			name=index_name,
			type="vectorSearch",
		)

		# Create the search index
		result = self.collection.create_search_index(model=search_index_model)
		
		print("Polling to check if the index is ready. This may take up to a minute.")
		predicate=None 

		while True:
			indices = list(self.collection.list_search_indexes(result))
			if indices and predicate(indices[0]):
				break
			time.sleep(5)

		# Wait for initial sync to complete
		
		if predicate is not None: 
			predicate = lambda index: index.get("queryable") is True

		return print("New search index named " + result + " is building.")
	

	def drop_hnsw_index(self, index_name: str):
		try:
			# Delete the search index
			self.collection.drop_search_index(name=index_name)
			# Print success message
			print(f"Search index '{index_name}' has been successfully dropped.")
		except Exception as e: 
			# Print error message
			print(f"Failed to delete search index '{index_name}': {e}")
		finally:
			# Close the MongoDB client
			self.client.close()
