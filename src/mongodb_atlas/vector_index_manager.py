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


	def is_readys(self,index_def: dict) -> bool:
		return (bool(index_def.get("queryable")) or index_def.get("state") == "READY" or index_def.get("status") == "READY")

	def create_hnsw_index(self
		, index_name: str
		, dimensions: int
		, attribute_name: "embedding"
		, similarity: str # consine, dotProduct, euclidean
		, filter_attribute_names: list =None):
		
		fields = [
			{
				"type": 'vector',
				"path": attribute_name,
				"numDimensions": dimensions,
				"similarity": similarity
			}
		]

		# Add all provided filter fields
		if filter_attribute_names :
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
		predicate = self.is_readys
		
		deadline = time.time() + 60 
		while time.time() < deadline:
			indices = list(self.collection.list_search_indexes(result))
			if indices and predicate(indices[0]):
				return print("New search index named " + result + " is building.")
			time.sleep(5)
		return print("Failed to create search index. Please check the logs.")
	

	def drop_hnsw_index(self, index_name: str):
		try:
			self.collection.drop_search_index(name=index_name)
			print(f"Search index '{index_name}' has been successfully dropped.")
		except Exception as e:
			print(f"Failed to delete search index '{index_name}': {e}")
		finally:
			self.client.close()

