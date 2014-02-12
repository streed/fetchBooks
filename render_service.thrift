namespace py fetchBooks

/*
  Current status for the job input.
*/
enum FetchBooksStatus {
  STARTING = 0,
  RUNNING = 1,
  ERROR = 2
}

struct FetchBooksError {
  1:FetchBooksStatus lastStatus,
  2:string error_string,
  3:string node_address,
  4:i64 id
}

struct FetchBooksResponse { 
  1:i64 id,
  2:i64 timestamp,
  3:FetchBooksStatus status = FetchBooksStatus.START,
  4:optional list<string> outputs,
  5:optional FetchBookError error
}

/*
  The food object.
*/
struct Food {
  1:i32 id,
  2:string name,
  3:i32 total_items,
  4:i32 single_item_price,
}

typedef list<Food> FoodList

/*
  The order object.
*/
struct Order {
  1:i64 id,
  2:i32 total_cost,
  3:FoodList food
}

typedef list<Order> OrderList

/* 
  The Invoice object
*/
struct Invoice {
  1:i64 id,
  2:string restaurant_name,
  3:string restaurant_address,
  4:string restaurant_contact,
  5:OrderList orders
  6:i64 invoice_total,
  7:i64 invoice_fee_total
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
  FetchBooksStatus render_invoice( 1:Invoice invoice ),
  FetchBooksStatus get_update( 1:FetchBooksStatus currentStatus )
}
