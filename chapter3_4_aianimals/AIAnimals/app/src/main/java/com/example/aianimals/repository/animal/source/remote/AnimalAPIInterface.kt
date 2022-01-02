package com.example.aianimals.repository.animal.source.remote

import retrofit2.Response
import retrofit2.http.*

interface AnimalAPIInterface {
    @Headers("Accept:application/json, Content-Type:application/json")
    @GET("/v0/metadata")
    suspend fun getMetadata(@Header("token") token: String): Response<MetadataResponse>

    @Headers("Accept:application/json, Content-Type:application/json")
    @POST("/v0/animal/search")
    suspend fun postSearchAnimal(
        @Header("token") token: String,
        @Query("limit") limit: Int = 100,
        @Query("offset") offset: Int = 0,
        @Body post: AnimalSearchPost
    ): Response<AnimalSearchResponse>

    @Headers("Accept:application/json, Content-Type:application/json")
    @GET("/v0/animal")
    suspend fun getAnimal(
        @Header("token") token: String,
        @Query("id") id: String,
        @Query("deactivated") deactivated: Boolean = false,
        @Query("limit") limit: Int = 1,
        @Query("offset") offset: Int = 0,
    ): Response<List<AnimalResponse>>
}