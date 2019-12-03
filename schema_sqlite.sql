-- ################## TABLES ################## --

CREATE TABLE `users` (
  `user_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `registered_at` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
  `last_login` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
  `username` VARCHAR(255),
  `password` VARCHAR(200),
  `email` VARCHAR(200)
);

CREATE TABLE `books` (
  `isbn` INTEGER NOT NULL PRIMARY KEY,
  `book_name` VARCHAR(255),
  `book_price` NUMERIC,
  `author` VARCHAR(255),
  `genre` VARCHAR(255)
);


CREATE TABLE `copies` (
  `copy_id` INTEGER NOT NULL PRIMARY KEY,
  `availability` INTEGER,
  `isbn` INTEGER,
  FOREIGN KEY(isbn) REFERENCES books(isbn)
);

CREATE TABLE `transactions` (
  `transaction_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `start_date` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
  `fees_due` INTEGER,
  `copy_id` INTEGER,
  `user_id` INTEGER,
  FOREIGN KEY(copy_id) REFERENCES copies(copy_id)
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);


-- ################## TRIGGERS ################## --

CREATE TRIGGER `triggerUserLogin` AFTER UPDATE ON `users`
BEGIN
   update `users` SET `last_login` = (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) WHERE id = NEW.id;
END;
