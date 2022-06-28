-- Keep a log of any SQL queries you execute as you solve the mystery.

-- List all the crimes from July, 28 2021 on Humphrey Street
SELECT * FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';
-- id: 295 -> @10:15am / interviews 3 witnesses -> bakery

-- list all the interviews from July, 28 2021
SELECT * FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;
-- ids: 161, 162, 163 -> thief withdraw money from the ATM on Leggett Street -> earliest flight of Fiftyville on July, 29th -> phonecall < 1min

-- find the bank account from atm_transactions -> find person_id from bank_accounts using account_number
SELECT account_number FROM atm_transactions WHERE day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

SELECT person_id
FROM bank_accounts
WHERE account_number IN(
    SELECT account_number
    FROM atm_transactions
    WHERE day = 28
    AND atm_location = 'Leggett Street'
    AND transaction_type = 'withdraw'
    );

-- list phonecalls from 28th July that last < 1min -> receive phone no
SELECT caller, receiver FROM phone_calls WHERE day = 28 AND duration < 60;

-- list name of people that used ATM and phone called on 28th July < 1min duration
SELECT *
FROM people, bank_accounts
WHERE people.id = bank_accounts.person_id
AND person_id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN(
        SELECT account_number
        FROM atm_transactions
        WHERE day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw'
        )
)
AND people.phone_number IN (
    SELECT caller
    FROM phone_calls
    WHERE day = 28
    AND duration < 60
);

-- list the license_plate from bakery around 10:25am on 28th -> exit
SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;

-- list people that matches all the above
SELECT *
FROM people, bank_accounts
WHERE people.id = bank_accounts.person_id
AND person_id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw'
        )
)
AND people.phone_number IN (
    SELECT caller
    FROM phone_calls
    WHERE day = 28
    AND duration < 60
)
AND people.license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE day = 28
    AND hour = 10
    AND minute BETWEEN 15 AND 25
);

-- +--------+-------+----------------+-----------------+---------------+----------------+-----------+---------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate | account_number | person_id | creation_year |
-- +--------+-------+----------------+-----------------+---------------+----------------+-----------+---------------+
-- | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       | 49610011       | 686048    | 2010          |
-- | 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       | 26013199       | 514354    | 2012          |
-- +--------+-------+----------------+-----------------+---------------+----------------+-----------+---------------+

-- list all flights from Fiftyville on 29th July
SELECT id FROM airports WHERE city = 'Fiftyville'; -- Fiftyville airport id

-- earliest flight from Fifthyville on 29th July -- id 36
SELECT flights.id FROM flights, airports WHERE origin_airport_id = airports.id AND day = 29 AND hour = (SELECT MIN(hour) FROM flights WHERE day = 29) AND origin_airport_id = (
    SELECT id FROM airports WHERE city = 'Fiftyville'
);

-- list all passengers from that flight
SELECT * FROM passengers JOIN flights ON flight_id = flights.id WHERE flight_id = (
    SELECT flights.id FROM flights, airports
    WHERE origin_airport_id = airports.id
    AND day = 29
    AND hour = (SELECT MIN(hour) FROM flights WHERE day = 29)
    AND origin_airport_id = (
        SELECT id FROM airports
        WHERE city = 'Fiftyville'
    )
);

-- get the passport no of the person from the flight that matches on passport_number with the one of the persons from above
SELECT * FROM passengers
JOIN flights ON flight_id = flights.id
WHERE flight_id = (
    SELECT flights.id
    FROM flights, airports
    WHERE origin_airport_id = airports.id
    AND day = 29
    AND hour = (SELECT MIN(hour) FROM flights WHERE day = 29)
    AND origin_airport_id = (
        SELECT id FROM airports
        WHERE city = 'Fiftyville'
    )
) AND passport_number IN (
        SELECT passport_number
        FROM people, bank_accounts
        WHERE people.id = bank_accounts.person_id
        AND person_id IN (
            SELECT person_id
            FROM bank_accounts
            WHERE account_number IN(
                SELECT account_number
                FROM atm_transactions
                WHERE day = 28
                AND atm_location = 'Leggett Street'
                AND transaction_type = 'withdraw'
                )
        )
        AND people.phone_number IN (
            SELECT caller
            FROM phone_calls
            WHERE day = 28
            AND duration < 60
        )
        AND people.license_plate IN (
            SELECT license_plate
            FROM bakery_security_logs
            WHERE day = 28
            AND hour = 10
            AND minute BETWEEN 15 AND 25
        )
);

-- get the person name with above passport id -> BRUCE
SELECT name
FROM people
WHERE passport_number = (
        SELECT passport_number
        FROM passengers
        JOIN flights ON flight_id = flights.id
        WHERE flight_id = (
            SELECT flights.id
            FROM flights, airports
            WHERE origin_airport_id = airports.id
            AND day = 29
            AND hour = (SELECT MIN(hour) FROM flights WHERE day = 29)
            AND origin_airport_id = (
                SELECT id
                FROM airports
                WHERE city = 'Fiftyville'
        )
    ) AND passport_number IN(
            SELECT passport_number
            FROM people, bank_accounts
            WHERE people.id = bank_accounts.person_id
            AND person_id IN (
                SELECT person_id
                FROM bank_accounts
                WHERE account_number IN(
                    SELECT account_number
                    FROM atm_transactions
                    WHERE day = 28
                    AND atm_location = 'Leggett Street'
                    AND transaction_type = 'withdraw'
                    )
            )
            AND people.phone_number IN (
                SELECT caller
                FROM phone_calls
                WHERE day = 28
                AND duration < 60
            )
            AND people.license_plate IN (
                SELECT license_plate
                FROM bakery_security_logs
                WHERE day = 28
                AND hour = 10
                AND minute BETWEEN 15 AND 25
            )
    )
);

-- the destination airport / city:
SELECT city
FROM airports
WHERE airports.id = (
    SELECT destination_airport_id
    FROM flights, airports
    WHERE origin_airport_id = airports.id
    AND day = 29
    AND hour = (SELECT MIN(hour) FROM flights WHERE day = 29)
    AND origin_airport_id = (
        SELECT id
        FROM airports
        WHERE city = 'Fiftyville'
    )
);

-- find who Bruce called
SELECT name
FROM people
WHERE phone_number = (
    SELECT receiver
    FROM phone_calls
    WHERE day = 28
    AND duration < 60
    AND caller = (
        SELECT phone_number
        FROM people
        WHERE name = 'Bruce'
    )
);
