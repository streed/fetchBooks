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
struct Item {
  1:string name,
  2:i32 qty,
  3:i64 subtotal,
  4:i64 total
}

typedef list<Item> Food

/*
  The order object.
*/
struct Order {
  1:i64 id,
  2:i64 total, 
  3:string order_date,
  4:Food food
}

struct Restaurant {
  1:Order order
}

typedef list<Restaurant> Restaurants

/* 
  The Invoice object
*/
struct Invoice { 
  1:Restaurants restaurants
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
