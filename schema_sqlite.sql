-- ################## TABLES ################## --

CREATE TABLE `users` (
  `user_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `registered_at` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
  `last_login` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
  `username` VARCHAR(255),
  `password` VARCHAR(200),
  `email` VARCHAR(200),
  `phone_number` VARCHAR(200),
  `street` VARCHAR(200),
  `city` VARCHAR(200),
  `state` VARCHAR(200)
);

CREATE TABLE `staff` (
  `user_id` INTEGER,
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE `books` (
  `isbn` INTEGER NOT NULL PRIMARY KEY,
  `book_name` VARCHAR(255),
  `book_price` NUMERIC,
  `author` VARCHAR(255),
  `genre` VARCHAR(255)
);


CREATE TABLE `copies` (
  `copy_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `availability` INTEGER,
  `isbn` INTEGER,
  FOREIGN KEY(isbn) REFERENCES books(isbn)
);

CREATE TABLE `transactions` (
  `transaction_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `start_date` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
  `fees_due` INTEGER DEFAULT 0,
  `returned` INTEGER DEFAULT 0,
  `copy_id` INTEGER,
  `user_id` INTEGER,
  FOREIGN KEY(copy_id) REFERENCES copies(copy_id)
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE `users_transactions` (
  `user_id` INTEGER,
  `transaction_id` INTEGER,
  FOREIGN KEY(user_id) REFERENCES users(user_id)
  FOREIGN KEY(transaction_id) REFERENCES transactions(transaction_id)
);


-- ################## TRIGGERS ################## --

CREATE TRIGGER `triggerUserLogin` AFTER UPDATE ON `users`
BEGIN
   update `users` SET `last_login` = (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) WHERE id = NEW.id;
END;

CREATE TRIGGER `userDelete_staff` AFTER DELETE ON `users`
FOR EACH ROW
BEGIN
DELETE FROM staff
    WHERE staff.user_id = old.user_id;
END;
