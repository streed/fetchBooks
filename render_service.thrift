namespace py fetchBooks

/*
  Current status for the job input.
*/
enum FetchBooksStatus {
  OK = 0,
  ERROR = 1
}

struct FetchBooksResponse { 
  1:i64 timestamp,
  2:FetchBooksStatus status = FetchBooksStatus.OK,
  3:string invoiceUrl
}

/*
  The food object.
*/
struct Food {
  1:i32 id,
  2:string item,
  3:string description
  4:i32 quantity,
  5:i32 unitCost
}

typedef list<Food> FoodList

/*
  The order object.
*/
struct Order {
  2:i32 subTotal,
  3:i32 tax,
  4:i32 discountPercentage,
  5:FoodList food
}

typedef list<Order> OrderList

/* 
  The Invoice object
*/
struct Invoice {
  1:i64 invoiceNumber,
  2:i64 invoiceDate,
  3:string restaurant_name,
  4:string restaurant_address,
  5:string restaurant_contact,
  6:Order order
}

/*
  This service provides the following functionality.

  Receiving an invoice and then generating a HTML/PDF 
  output from it.

  If the same invoice is sent then the same HTML/PDF
  document should be returned. I.E they should only
  be generated once.
*/
service FetchBooksService {
  FetchBooksResponse render_invoice( 1:Invoice invoice ),
}
