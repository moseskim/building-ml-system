package com.example.aianimals.listing.detail

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import com.example.aianimals.R
import com.example.aianimals.repository.Animal

class AnimalDetailFragment : Fragment(), AnimalDetailContract.View {
    override lateinit var presenter: AnimalDetailContract.Presenter
    private lateinit var tv_animal_name: TextView
    private lateinit var tv_animal_price: TextView
    private lateinit var tv_animal_purchase_date: TextView

    override fun showAnimal(animal: Animal) {
        tv_animal_name.text = animal.name
        tv_animal_price.text = animal.price.toString()
        tv_animal_purchase_date.text = animal.date
        tv_animal_name.visibility = View.VISIBLE
        tv_animal_price.visibility = View.VISIBLE
        tv_animal_purchase_date.visibility = View.VISIBLE
    }

    override fun onResume() {
        super.onResume()
        presenter.start()
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val root = inflater.inflate(R.layout.animal_detail_fragment, container, false)

        with (root)
        {
            activity?.title = getString(R.string.item_detail)
            tv_animal_name = findViewById(R.id.tv_animal_name)
            tv_animal_price = findViewById(R.id.tv_animal_price)
            tv_animal_purchase_date = findViewById(R.id.tv_animal_purchase_date)
//            setFragmentResultListener("animalData") {_, bundle ->
//                tv_animal_name.text = bundle.getString("animalName")
//                tv_animal_price.text = bundle.getInt("animalPrice").toString()
//                tv_animal_purchase_date.text = bundle.getString("animalPurchaseDate")
//            }
        }
        return root
    }

    companion object {

        private val ARGUMENT_ANIMAL_ID = "ANIMAL_ID"

        fun newInstance(animalID: Int) =
            AnimalDetailFragment().apply {
                arguments = Bundle().apply { putInt(ARGUMENT_ANIMAL_ID, animalID) }
            }
    }
}