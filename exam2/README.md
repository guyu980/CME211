Writeup

To deal with this problem, I design two classes.
The input argument of the first Inventorry class is the invetory file name. It contains:
1. Vector items to store the item names, map item_price and item_qty to store the price and quantity of items.
2. Revenue and change during one transaction.
3. In the constructor, the class will load the inventory data.
4. Five methods:
  (1) Print method to print the current stock.
  (2) AttemptExport method to make a transaction attempt, with the input arguements (item, qty, funds).
      First judge whether the input is extrem case, like item not in the inventory or qty / funds is negtive.
      Then figure out whether there is enough quantity of item, and update actual sell quantity by how 
      many item the funds is enough to pay for. Finally calculate revenue and change during this transaction.
  (3) SummarizeTransaction method to report revenue and changes.
  (4) TotalStock and Value are methods to report current total stock and value

The second class CashRegister has input arguement change.
It only has one method Print to report changes in different types of money.
