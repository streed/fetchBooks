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
  3:double subtotal,
  4:double total,
  5:double tax
}

typedef list<Item> Food

/*
  The order object.
*/
struct Order {
  1:i64 id,
  2:double subtotal, 
  2:double tax, 
  2:double total, 
  3:string order_date,
  4:Food food
}

struct Restaurant {
  1:string name,
  2:Order order
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
