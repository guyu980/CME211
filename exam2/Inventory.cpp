#include "Inventory.hpp"
#include "CashRegister.hpp"

#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>

Inventory::Inventory (std::string inventory_fname) {
    this->inventory_fname = inventory_fname;
    float price;
    int qty;
    std::string item;
    std::ifstream f(inventory_fname);
    std::stringstream line;
    
    /* Load data */
    if (f.is_open())
        while (f >> item >> price >> qty) {
            items.push_back(item);
            item_price[item] = price;
            item_qty[item] = qty;
        }
    else
        std::cout << "Failed to open input file!" << std::endl;
}

/* Method to print the current stock */
void Inventory::Print(void) {
    int n_item = (int) items.size();
    
    for (int i = 0; i < n_item; i++) {
        std::cout << items[i] << std::endl;
        std::cout << "    " << item_price[items[i]] << ", " << item_qty[items[i]] << std::endl;
    }
}

/* Method to make a transaction attempt */
int Inventory::AttemptExport(std::string item, int qty, float funds) {
    int qty_sell;
    
    /* Report message in extreme cases */
    if (item_qty.count(item) == 0 || item_qty[item] == 0) {
        std::cout << "No stock of this item!" << std::endl;
        return 0;
    }
    
    if (qty < 0) {
        std::cout << "Client attempts to sell!" << std::endl;
        return 0;
    }
    
    if (funds < 0) {
        std::cout << "Client attempts to rob!" << std::endl;
        return 0;
    }
    
    /* Whether there is enough quantity */
    if (item_qty[item] < qty)
        qty_sell = item_qty[item];
    else
        qty_sell = qty;
    
    revenue = item_price[item] * qty_sell;
    
    /* Update acutal selling quantity by whether funds is enough */
    if (funds < revenue) {
        qty_sell = (int) (funds / item_price[item]);
    }
    
    /* Compute the revenue and change */
    item_qty[item] -= qty_sell;
    revenue = item_price[item] * qty_sell;
    change = funds - revenue;
    
    /* Store current inventory into file */
    std::ofstream of(inventory_fname);
    
    if (of.is_open()) {
        for  (int i = 0; i < (int) items.size(); i++)
            of << items[i] << ", " << item_price[items[i]] << ", " << item_qty[items[i]] << std::endl;
        of.close();
    }
    else
        std::cout << "Failed to open output file!" << std::endl;
    
    return 1;
}


/* Method to report revenue and changes */
float Inventory::SummarizeTransaction(void) {
    CashRegister cash(change);
    cash.Print();
    return revenue;
}


/* Method to report current total stock */
int Inventory::TotalStock(void) {
    int stock = 0, n_item = (int) items.size();
    
    for (int i = 0; i < n_item; i++)
        stock += item_qty[items[i]];
    
    return stock;
}


/* Method to report current total value */
float Inventory::Value(void) {
    float value = 0;
    int n_item = (int) items.size();

    for (int i = 0; i < n_item; i++)
        value += item_qty[items[i]] * item_price[items[i]];
    
    return value;
}
