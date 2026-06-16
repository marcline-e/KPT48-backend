from app.database.mysql import get_db_connection


def get_event_by_id(event_id):
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            query = """
                SELECT
                    id_event,
                    total_quota,
                    status
                FROM events
                WHERE id_event = %s
            """

            cursor.execute(query, (event_id,))
            result = cursor.fetchone()

            if not result:
                return None

            return {
            "event_id": result["id_event"],
            "quota": result["total_quota"],
            "status": result["status"]
        }

    finally:
        conn.close()


def get_pending_registrants(event_id):
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            query = """
                SELECT
                    tr.id_ticket_registration,
                    u.id_user,
                    u.username,
                    COALESCE(op.loss_count, 0) AS loss_count
                FROM ticket_registrations tr
                JOIN users u
                    ON tr.id_user = u.id_user
                LEFT JOIN official_profiles op
                    ON u.id_user = op.id_user
                WHERE
                    tr.id_event = %s
                    AND tr.status = 'PENDING'
                    AND tr.phase = 'OFFICIAL'
            """

            cursor.execute(query, (event_id,))
            results = cursor.fetchall()

            return [
                {
                    "ticket_id": row["id_ticket_registration"],
                    "user_id": row["id_user"],
                    "username": row["username"],
                    "loss_count": row["loss_count"]
                }
                for row in results
            ]

    finally:
        conn.close()


# def update_ticket_status(ticket_id, status):
#     conn = get_db_connection()

#     try:
#         with conn.cursor() as cursor:
#             query = """
#                 UPDATE ticket_registrations
#                 SET status = %s
#                 WHERE id_ticket_registration = %s
#             """

#             cursor.execute(
#                 query,
#                 (status, ticket_id)
#             )

#         conn.commit()

#     finally:
#         conn.close()


# def reset_loss_count(user_id):
#     conn = get_db_connection()

#     try:
#         with conn.cursor() as cursor:
#             query = """
#                 UPDATE official_profiles
#                 SET loss_count = 0
#                 WHERE id_user = %s
#             """

#             cursor.execute(
#                 query,
#                 (user_id,)
#             )

#         conn.commit()

#     finally:
#         conn.close()


# def increment_loss_count(user_id):
#     conn = get_db_connection()

#     try:
#         with conn.cursor() as cursor:
#             query = """
#                 UPDATE official_profiles
#                 SET loss_count = loss_count + 1
#                 WHERE id_user = %s
#             """

#             cursor.execute(
#                 query,
#                 (user_id,)
#             )

#         conn.commit()

#     finally:
#         conn.close()


def batch_update_ticket_status(ticket_ids, status):
    if not ticket_ids:
        return

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:

            placeholders = ",".join(
                ["%s"] * len(ticket_ids)
            )

            query = f"""
                UPDATE ticket_registrations
                SET status = %s
                WHERE id_ticket_registration IN ({placeholders})
            """

            cursor.execute(
                query,
                [status] + ticket_ids
            )

        conn.commit()

    finally:
        conn.close()


def batch_reset_loss_count(user_ids):
    if not user_ids:
        return

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:

            placeholders = ",".join(
                ["%s"] * len(user_ids)
            )

            query = f"""
                UPDATE official_profiles
                SET loss_count = 0
                WHERE id_user IN ({placeholders})
            """

            cursor.execute(
                query,
                user_ids
            )

        conn.commit()

    finally:
        conn.close()


def batch_increment_loss_count(user_ids):
    if not user_ids:
        return

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:

            placeholders = ",".join(
                ["%s"] * len(user_ids)
            )

            query = f"""
                UPDATE official_profiles
                SET loss_count = loss_count + 1
                WHERE id_user IN ({placeholders})
            """

            cursor.execute(
                query,
                user_ids
            )

        conn.commit()

    finally:
        conn.close()