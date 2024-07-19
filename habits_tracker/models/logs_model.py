from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, Union, Optional
from datetime import date, datetime
from uuid import UUID

from supabase import Client


class LogsModel(ABC):
    @abstractmethod
    def create_log_single(self, habit_id: UUID, log_date: date, log_value: Union[int, float]) -> None:
        pass

    @abstractmethod
    def create_logs_for_date(self, log_form: Dict[date, Dict[UUID, Union[int, float]]]) -> None:
        pass

    @abstractmethod
    def retrieve_logs_for_date(self, user_id: UUID, log_date: date) -> Dict[UUID, Union[int, float]]:
        ''' Should return {"habit1": value, "habit2": value, ...}'''
        pass

    @abstractmethod
    def retrieve_user_logs(self, user_id: UUID, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Dict[date, Dict[UUID, Union[int, float]]]:
        '''
        if start_date and end_date not specified will return all
        Should return {"date1": {"habit1": value, "habit2": value}, ... }
        '''
        pass


class SupabaseLogsModel(LogsModel):
    def __init__(self, supabase_client: Client):
        self.client: Client = supabase_client

    def create_log_single(self, habit_id: str, log_date: date, log_value: Union[int, float]) -> None:
        data = {
            "habit_id": habit_id,
            "log_date": log_date.isoformat(),
            "log_value": log_value,
            "updated_at": datetime.now().isoformat()  # Update the updated_at timestamp
        }
        # Check if the log entry exists
        existing_log = self.client.table('logs').select('log_id').eq('habit_id', habit_id).eq('log_date', log_date.isoformat()).execute()

        if existing_log.data:
            # Update the existing log entry
            log_id = existing_log.data[0]['log_id']
            self.client.table('logs').update(data).eq('log_id', log_id).execute()
        else:
            # Insert a new log entry
            self.client.table('logs').insert(data).execute()

    def create_logs_for_date(self, log_form: Dict[date, Dict[str, Union[int, float]]]) -> None:
        for log_date, logs in log_form.items():
            for habit_id, log_value in logs.items():
                self.create_log_single(habit_id, log_date, log_value)

    def retrieve_logs_for_date(self, user_id: UUID, log_date: date) -> Dict[str, Union[int, float]]:
        query = self.client.table('logs').select("*, habits(*)")
        query = query.eq('log_date', log_date.isoformat())
        query = query.eq('habits.user_id', user_id)
        response = query.execute()
        logs = response.data

        log_dict = {}
        for log in logs:
            habit_name = log['habits']['habit_name']
            log_type = log['habits']['habit_type']
            log_value_raw = log['log_value']
            log_value = self.convert_value(log_value_raw, log_type)

            log_dict[habit_name] = {"value": log_value, "type": log_type}
        return log_dict

    def retrieve_user_logs(self, user_id: str, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Dict[date, Dict[str, Union[int, float]]]:
        query = self.client.table('logs').select('*, habits(*)').eq('habits.user_id', user_id)

        if start_date:
            query = query.gte('log_date', start_date.isoformat())
        if end_date:
            query = query.lte('log_date', end_date.isoformat())

        response = query.execute()
        logs = response.data

        user_logs = defaultdict(dict)
        for log in logs:
            log_date = datetime.fromisoformat(log['log_date']).date()
            habit_name = log['habits']['habit_name']
            log_value_raw = log['log_value']
            log_type = log['habits']['habit_type']
            log_value = self.convert_value(log_value_raw, log_type)

            print(log_date, habit_name, log_value, log_type)
            user_logs[str(log_date)][habit_name] = {"value": log_value, "type": log_type}
            print(user_logs)

        return user_logs

    def convert_value(self, value: Union[int, float], habit_type: str) -> Union[int, float, bool]:
        if habit_type == "boolean":
            return bool(value)
        return value
