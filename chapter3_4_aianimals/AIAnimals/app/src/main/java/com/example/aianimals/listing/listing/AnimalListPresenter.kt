package com.example.aianimals.listing.listing

import android.util.Log
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalRepository
import com.example.aianimals.repository.login.source.LoginRepository
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext

class AnimalListPresenter(
    private val animalRepository: AnimalRepository,
    private val loginRepository: LoginRepository,
    private val animalListView: AnimalListContract.View,
    private val appExecutors: AppExecutors = AppExecutors()
) : AnimalListContract.Presenter {
    private val TAG = AnimalListPresenter::class.java.simpleName

    override var token: String? = null
    override var query: String? = null

    init {
        this.animalListView.presenter = this
    }

    override fun start() {
        listAnimals(null, true)
    }

    override fun listAnimals(
        query: String?,
        refresh: Boolean
    ) = runBlocking {
        this@AnimalListPresenter.query = query
        setToken()
        var animals = mapOf<String, Animal>()
        withContext(appExecutors.ioContext) {
            if (token != null) {
                val metadata = animalRepository.getMetadata(token!!)
                Log.i(TAG, "metadata: ${metadata}")
            }
            animals = animalRepository.listAnimals(this@AnimalListPresenter.query)
        }
        animalListView.showAnimals(animals)
    }

    override fun setToken() = runBlocking {
        withContext(appExecutors.ioContext) {
            val login = loginRepository.isLoggedIn()
            if (login != null) {
                token = login.token!!
            }
        }
    }

    override fun logout() = runBlocking {
        withContext(appExecutors.ioContext) {
            loginRepository.logout()
        }
    }
}