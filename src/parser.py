class Parsers:
    @staticmethod
    def parse_turn_completed(payload):
        if payload.get("method") == "turn/completed":
            params = payload.get("params", {})
            return params.get("turn", {}).get("id")
        return None

    @staticmethod
    def parse_thread_read(payload):
        if "result" in payload:
            return payload["result"].get("thread", {}).get("id")
        return None

    @staticmethod
    def parse_thread_turns_list(payload):
        if "result" in payload:
             turns = payload["result"].get("turns", [])
             if turns:
                 return turns[-1].get("id")
        return None

    @staticmethod
    def correlate_backend(turn_completed_event, thread_read_response, turns_list_response, client_msg_id):
        # 1. Turn Completed Event matches
        turn_id = Parsers.parse_turn_completed(turn_completed_event)
        if not turn_id: return False

        # 2. Status Completed
        if turn_completed_event.get("params", {}).get("turn", {}).get("status") != "completed":
            return False

        # 3. Readback correlation
        read_thread_id = Parsers.parse_thread_read(thread_read_response)
        list_turn_id = Parsers.parse_thread_turns_list(turns_list_response)

        if not read_thread_id: return False
        if list_turn_id != turn_id: return False

        # 4. Client message ID correlation
        user_msg = None
        for turn in turns_list_response.get("result", {}).get("turns", []):
             if turn.get("id") == turn_id:
                 for msg in turn.get("messages", []):
                     if msg.get("author", {}).get("role") == "user":
                         user_msg = msg
                         break

        if not user_msg: return False
        if user_msg.get("clientId") != client_msg_id: return False

        return True
