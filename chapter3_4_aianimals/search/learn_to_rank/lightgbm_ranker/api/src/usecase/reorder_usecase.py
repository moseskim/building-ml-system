from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

import pandas as pd
from fastapi import BackgroundTasks
from src.configurations import Configurations
from src.infrastructure.cache_client import AbstractCacheClient
from src.infrastructure.db_client import AbstractDBClient
from src.repository.animal_repository import AnimalQuery, AnimalRepository
from src.schema.animal import AnimalRequest, AnimalResponse
from src.service.learn_to_rank_predict_service import AbstractLearnToRankPredictService

logger = getLogger(__name__)


def make_query_id(
    phrases: str,
    animal_category_id: Optional[int],
    animal_subcategory_id: Optional[int],
) -> str:
    return f"{Configurations.model_name}_{phrases}_{animal_category_id}_{animal_subcategory_id}"


class AbstractReorderUsecase(ABC):
    def __init__(
        self,
        animal_repository: AnimalRepository,
        db_client: AbstractDBClient,
        cache_client: AbstractCacheClient,
        learn_to_rank_predict_service: AbstractLearnToRankPredictService,
    ):
        self.animal_repository = animal_repository
        self.db_client = db_client
        self.cache_client = cache_client
        self.learn_to_rank_predict_service = learn_to_rank_predict_service

    @abstractmethod
    def reorder(
        self,
        request: AnimalRequest,
        background_tasks: BackgroundTasks,
    ) -> AnimalResponse:
        raise NotImplementedError


class ReorderUsecase(AbstractReorderUsecase):
    def __init__(
        self,
        animal_repository: AnimalRepository,
        db_client: AbstractDBClient,
        cache_client: AbstractCacheClient,
        learn_to_rank_predict_service: AbstractLearnToRankPredictService,
    ):
        super().__init__(
            animal_repository=animal_repository,
            db_client=db_client,
            cache_client=cache_client,
            learn_to_rank_predict_service=learn_to_rank_predict_service,
        )

    def __set_prediction_cache(
        self,
        query_id: str,
        ordered_animal_ids: List[str],
    ):
        self.cache_client.set(
            key=query_id,
            value=",".join(ordered_animal_ids),
        )

    def reorder(
        self,
        request: AnimalRequest,
        background_tasks: BackgroundTasks,
    ) -> AnimalResponse:
        query_phrases = ".".join(request.query_phrases)
        query_id = make_query_id(
            phrases=query_phrases,
            animal_category_id=request.query_animal_category_id,
            animal_subcategory_id=request.query_animal_subcategory_id,
        )
        cached_data = self.cache_client.get(key=query_id)
        if cached_data is not None:
            return AnimalResponse(ids=cached_data.split(","))
        animal_query = AnimalQuery(ids=request.ids)
        animals = self.animal_repository.select_all(animal_query=animal_query)
        input_dict = [
            dict(
                animal_id=a.id,
                animal_category_id=a.animal_category_id,
                animal_subcategory_id=a.animal_subcategory_id,
                name=a.name,
                description=a.description,
                query_phrases=query_phrases,
                query_animal_category_id=request.query_animal_category_id,
                query_animal_subcategory_id=request.query_animal_subcategory_id,
            )
            for a in animals
        ]
        input_df = pd.DataFrame(input_dict)
        prediction = self.learn_to_rank_predict_service.predict(input=input_df)
        ordered_animal_ids = [p[0] for p in prediction]
        background_tasks.add_task(
            self.__set_prediction_cache,
            query_id,
            ordered_animal_ids,
        )
        return AnimalResponse(ids=ordered_animal_ids)
