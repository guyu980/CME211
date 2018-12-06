#ifndef Inventory_hpp
#define Inventory_hpp

#include <string>
#include <vector>
#include <map>

class Inventory {
  private:
    float revenue, change;
    std::string inventory_fname;
    std::vector<std::string> items;
    std::map<std::string, float> item_price;
    std::map<std::string, int> item_qty;
  public:
    Inventory(std::string inventory_fname);
    /* Method to print the current stock */
    void Print(void);
    /* Method to make a transaction attempt */
    int AttemptExport(std::string item, int qty, float funds);
    /* Method to report revenue and changes */
    float SummarizeTransaction(void);
    /* Method to report current total stock */
    int TotalStock(void);
    /* Method to report current total value */
    float Value(void);
};

#endif /* Inventory_hpp */
