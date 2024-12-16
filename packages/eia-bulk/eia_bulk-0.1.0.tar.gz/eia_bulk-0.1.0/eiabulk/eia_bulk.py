import requests
import pandas as pd
from sqlalchemy import create_engine
import time
from dotenv import load_dotenv
import os
import importlib.resources as pkg_resources
from collections.abc import Iterable
from collections import deque
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
import json
import types
from tenacity import retry, wait_full_jitter, stop_after_attempt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta



load_dotenv(verbose=True, override=True)


def check_iterable(to_check):
        return isinstance(to_check, Iterable) and not isinstance(to_check, str)

@retry(wait=wait_full_jitter(min=1, max=10), stop=stop_after_attempt(5))
def get_post(url, api_key, verbose):
    # Define the API endpoint URL
    full_api = url + "&api_key=" + api_key
    if verbose >= 2:
        print(f"API URL:{full_api}")
   
    # Make a GET request to the API endpoint using requests.get()
    response = requests.get(full_api)
    if response.status_code > 299 and verbose > 1:
        print(f"Error code: {response.status_code}")
    if response.status_code > 299 and verbose == 1:
        print(f"Error code: {response.status_code} URL: {full_api}")
    
        
 
    response.raise_for_status()

    # Check if the request was successful (status code 200)
    
    return response.json()
    
 

        
def num2str(date):
    if date//10==0:
        str_date = f"0{date}"
    else:
        str_date = str(date)
    return str_date


def generate_date_ranges(start_year, end_year, multiplier):
    """
    Generate date ranges split by a given multiplier in months.

    :param start_year: The starting year of the range (inclusive).
    :param end_year: The ending year of the range (inclusive).
    :param multiplier: The number of months (can be fractional) to split ranges by.
    :return: A list of tuples with start and end dates in 'YYYY-MM-DD' format.
    """
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year + 1, 1, 1)  # Add one year to include the full last year

    current_date = start_date
    ranges = []

    # Split the multiplier into whole months and fractional days
    whole_months = int(multiplier)
    extra_days = int((multiplier % 1) * 30.4375)  # Approximate fraction as days

    while current_date < end_date:
        # Add whole months and extra days to the current date
        next_date = current_date + relativedelta(months=whole_months) + timedelta(days=extra_days)
        if next_date > end_date:
            next_date = end_date

        ranges.append((current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d')))
        current_date = next_date

    return ranges






def split_month_dates(year, month=None, month_multiplier=None):
    def num2str(num):
        return f"{num:02d}"
    
 
    num_ranges = round(1/month_multiplier)
    # Get the total number of days in the given month
  
    total_days = calendar.monthrange(year, month)[1]
    if num_ranges > total_days:
        num_ranges = total_days
        
    # Calculate the interval size
    try:
        interval = total_days // num_ranges
    except:
        raise TypeError("Your multiplier must be smaller than or equal to 1 for smaller granularity information.")

    # Create the date ranges
    ranges = []
    for i in range(num_ranges):
        start_day = i * interval + 1
        end_day = (i + 1) * interval if i < num_ranges - 1 else total_days

        start_date = f"{year}-{num2str(month)}-{num2str(start_day)}"
        if i == num_ranges - 1:  # Last range
            end_date = f"{year}-{num2str(month)}-{num2str(total_days)}"
        else:
            end_date = f"{year}-{num2str(month)}-{num2str(end_day + 1)}"

        ranges.append((start_date, end_date))

    # Adjust the last range to spill over to the next month if necessary
    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year += 1

    if len(ranges) > 0:
        last_range_start, _ = ranges[-1]
        last_range_end = f"{next_year}-{num2str(next_month)}-01"
        ranges[-1] = (last_range_start, last_range_end)
    
    


    return ranges




def resp2df(response):
    try:   
        resp = response["response"]['data']
    except:
        raise Exception(f"Malformated Response Is likely to be an unexpected API return")
    df = pd.DataFrame(resp)
    return df







class EIABulk:
    def __init__(self, api_key=None, route=None,
        facet_types=[], sort=[], data_types=[], frequency=None,
        route0=None, route1=None, route2=None,  db_settings=None,
        host=None, dbname=None, username=None, password=None, tablename=None, write2db=None, override=False, 
        from_api=True, verbose=1, multiplier=None, sleep_between_calls=.4, 
        yield_df=True, use_original_route=False, large_granularity=False):
        
        self.verbose = verbose
        ###Warning Adjust at your own risk###
        self.sleep_between_calls = sleep_between_calls
        #####################################
        if self.sleep_between_calls < .4 and self.verbose >= 0:
            print("Warning: Having a lower time between calls may result in your key being temporarily or permanently disabled.\nIt should be noted that the time it takes to return the api call is subtracted from sleep_between_calls.")
        self.yield_df = yield_df
        self.use_original_route = use_original_route
        #Instantiating Variables
        self.override = override
        self.from_api = from_api
        self.host = None
        self.dbname = None
        self.username = None
        self.pwd = None
        self.tablename = None
        self.api_key = None
        self.route = None
        self.facets = None
        self.short_all_routes = {}
        self.all_routes = {}
        self.large_granularity = large_granularity
        
        try:
            if self.use_original_route:
                with pkg_resources.open_text('eiabulk.route_trees', 'og_route_tree.json') as f:
                    self.all_routes = json.load(f)
                with pkg_resources.open_text('eiabulk.route_trees', 'og_short_route_tree.json') as f:
                    self.short_all_routes = json.load(f)
            else:
                with pkg_resources.open_text('eiabulk.route_trees', 'updated_route_tree.json') as f:
                    self.all_routes = json.load(f)
                with pkg_resources.open_text('eiabulk.route_trees', 'updated_short_route_tree.json') as f:
                    self.short_all_routes = json.load(f)
        except:
            print("Warning one or more of your path_tree files appear to be missing. Try toggling use_original_route to True, otherwise if you would like to make use of the path_trees please run the eiabulk.update_tree function.")
            
        
        
        self.frequency = frequency
        if isinstance(facet_types, types.GeneratorType) or isinstance(data_types, types.GeneratorType) or isinstance(sort, types.GeneratorType) or isinstance(route, types.GeneratorType):
            raise TypeError("No support for generators.")
        
        if check_iterable(data_types):
            self.data = data_types
        else:
            self.data = [data_types]
        
        if check_iterable(facet_types) and len(facet_types) == 0:
            self.facets = facet_types
        elif check_iterable(facet_types) and check_iterable(facet_types[0]):
            self.facets = facet_types
        elif check_iterable(facet_types):
            self.facets = [facet_types]
        elif isinstance(facet_types, str):
            self.facets = [facet_types]
        else:
            raise TypeError("facet_types is not using any known format. Should be list of touples or a string. String only for viewing route options. Touples should contain two items the facet_type and facet_id.")
        if isinstance(sort, str):
           self.sort = [(sort, 'desc')]
        elif self.string_list(sort):
            self.sort = [(item, 'desc') for item in sort]
        elif self.tuple_list(sort):
            self.sort = sort
        else:
            raise TypeError("sort is not using any known format. Should be list of touples, a list of strings, or a singular string. String and list of strings option will default to descending order('desc'). The list of touples should contain two items the sort type and sort direction ('asc' or 'desc'). The list of strings should just contain the sort types.")
        
        if host is not None:
            self.host = host
        elif os.getenv("HOST"):
            self.host = str(os.getenv("HOST"))
        if dbname is not None:
            self.dbname = dbname
        elif os.getenv("DBNAME"):
            self.dbname = str(os.getenv("DBNAME"))
        if username is not None:
            self.username = username
        elif os.getenv("USERNAME"):
            self.username = str(os.getenv("USERNAME"))
        if password is not None:
            self.pwd = password
        elif os.getenv("PASSWORD"):
            self.pwd = str(os.getenv("PASSWORD"))
        if tablename is not None:
            self.tablename = tablename
        elif os.getenv("TABLENAME"):
            self.tablename = str(os.getenv("TABLENAME"))

        if db_settings is not None:
            if 'host' in db_settings:
                self.host = db_settings['host']
            if 'dbname' in db_settings:
                self.dbname = db_settings['dbname']
            if 'username' in db_settings:
                self.username = db_settings['username']
            if 'password' in db_settings:
                self.pwd = db_settings['password']
            if 'tablename' in db_settings:
                self.tablename = db_settings['tablename']


        if self.host and self.dbname and self.username and self.tablename and write2db is None:
            if self.verbose >= 0:
                print("Write to databases has been enabled by default since all credentials have been found. To disable writing to database set write2db to False.")
            self.write2db = True
        elif write2db is not None:
            self.write2db = write2db


        if route is None and (route0 is not None or route1 is not None or route2 is not None):
            route = []
            if route0 is not None:
                route.append(route0)
            if route1 is not None:
                route.append(route1)
            if route2 is not None:
                route.append(route2)

    
        
        if check_iterable(route):
            self.route = '/'.join(route)
        elif isinstance(route, str):
            self.route = route
        else:
            raise TypeError('The provided route variable is neither an iterable or string. route should be formatted route0/route1/route2 or route0/route1 or route0. Can be set manually with route as iterable or string. Can also be set with route0, route1, route2 variables. Check documentations for specific examples.')
        
        if api_key is not None:
            self.api_key = api_key
        elif os.getenv("EIA_KEY"):
            self.api_key = str(os.getenv("EIA_KEY"))
        else:
            raise ValueError(
                "EIA_KEY missing add to .env file, environment variables, or pass api key to api_key instance variable. May need to reset kernel once setting password in EIA_KEY if using jupyter notebook."
            )
        
        
        #Pure Error Catching
       
        if not self.route_is_formatted(self.route):
            raise ValueError("Route String it malformed. route should be formatted route0/route1/route2 or route0/route1 or route0. Can be set manually with route as iterable or string. Can also be set with route0, route1, route2 variables. Check documentations for specific examples.\n")
        
        if self.write2db is not None and not isinstance(write2db, bool):
            raise TypeError('write2db should be a boolean value.')
        if not route0 and not route1 and not route2 and not route:
            raise ValueError('Missing API route. route should be formatted route0/route1/route2 or route0/route1 or route0. Can be set manually with route as iterable or string. Can also be set with route0, route1, route2 variables. Check documentations for specific examples.\n')
        
        if db_settings and isinstance(db_settings, dict):
            raise TypeError("db_settings should be a dictionary.")
        self.enable_functions = self.is_supported()

        split_route = self.route.split('/')
        layer = None
        try:
                layer = self.search_nested_dict(split_route, self.all_routes)
        except:
            if self.verbose >= 0:
                print("Warning: The route you provided does not appear in the default available routes.\nIf you would like to make requests provide value for the frequency variable.\nYou may also want to manually set a data variable since you are likely not be recieve any data without a data variable set.\nIf you believe the route tree is outdated you can run the update_tree() function.\n")
        if self.frequency is None and layer is not None:
            self.frequency = layer['frequency'][0]
            if self.verbose >= 1:
                print(f"Warning: No frequency variable found. Will default to {self.frequency}.")
           
        if not self.data and layer is not None:
            if self.verbose >= 1:
                print("Warning: No data variable found. Will select all available data variables.\n")
            self.data = layer['data']
        if multiplier is not None:
            self.multiplier = multiplier
        elif self.frequency is None:
            self.multiplier = 1
        elif "hourly" in self.frequency or 'week' in self.frequency or 'daily' in self.frequency:
            self.multiplier = .5
        elif 'monthly' in self.frequency or 'quarterly' in self.frequency:
                self.multiplier = 6
        elif 'yearly' in self.frequency:
            self.multiplier = 72
        else:
            self.multiplier = 6

        if not self.enable_functions and self.verbose >= 0:
            print("WARNING: The route you provided or the other search settings you have provided do not appear to be supported by the data collection API.\n If you would like to use the data API functions regardless it is likely to result in an invalid API call.\nIf you believe the route tree is outdated you can run the update_tree() function.\n")
        
        if self.override:
            self.enable_functions = True
        

    def __str__(self):
        return self.route_endpoints()

    
    @staticmethod
    def validate_iterables(validation_copy):   
        for inner in validation_copy:
            # Ensure each item in the outer iterable is itself an iterable
            if check_iterable(inner):
                raise TypeError(f"Expected an iterable, but got {type(inner)}: {inner}")
            
            # Convert the inner iterable to a list to check its length
            inner_list = list(inner)
            if len(inner_list) != 2:
                raise ValueError(f"Inner iterable must have exactly 2 elements, but got {len(inner_list)}: {inner_list}")
            
            # Ensure both elements of the inner iterable are strings
            if not all(isinstance(item, str) for item in inner_list):
                raise TypeError(f"All elements of the inner iterable must be strings, but got: {inner_list}")
        
        # Return the original iterable for further use
    
    def tuple_list(self, validation_copy):
        # Create a duplicate of the generator (or iterable) to avoid consuming it
        
        
        if not check_iterable(validation_copy):
            return False
        for inner in validation_copy:
            # Ensure each item in the outer iterable is itself an iterable
            if not check_iterable(inner):
                return False
            
            # Convert the inner iterable to a list to check its length
            
            # Ensure both elements of the inner iterable are strings
            if not all(isinstance(item, str) for item in inner):
                raise False
        return True
        # Return the original iterable for further use 
    def string_list(self, iter):
        if not check_iterable(iter):
            return False
        if not all(isinstance(item, str) for item in iter):
            return False
        return True
    @staticmethod
    def route_is_formatted(string):
        pattern = r'^[^/]+(?:/[^/]+)*$'

        # Match the input string against the regular expression pattern
        if re.match(pattern, string):
            return True
        else:
            return False
        
    @staticmethod
    def check_list_single(facet_list):
        
        if len(facet_list) == 1 and isinstance(facet_list[0], str):
            return True
        return False
    
        
    
    def route_endpoints(self):
        
        split_route = self.route.split('/')
        
        if len(self.facets) > 1:
                raise ValueError("If you are seeking route information provide a list containing only one facet_type.")
        if self.from_api:
            if self.verbose >= 2:
                print("This function will provide information about the available facets if you provide a facet type.\n If you only provide a valid route then it will give you information about the next available path\nor if its an endpoint it will provide information about the available facet types, available data types, frequency types, and sort options.\n")
                print("By default will print result from API. You can change this by setting the form_api variable to False.")
            return json.dumps(self.route_info(), indent=2)
        else:
            
            try:
                
                if self.verbose >= 2:
                    print(f"The following are the potential routes/features one can pick from given endpoint: {self.route}")
                layer = self.search_nested_dict(split_route, self.short_all_routes)
                if 'frequency' in layer:
                    return json.dumps(self.search_nested_dict(split_route, self.all_routes), indent=2)
                else:
                    return json.dumps(layer, indent=2)
                
            except:
                return "The route you have provided does not appear in the default available routes and is unable to print furthur options. Try setting the from_api instance variable to True."

    def is_supported(self):
        split_route = self.route.split('/')
        try:
            layer = self.search_nested_dict(split_route, self.all_routes)
        except:
            if self.verbose >= 0:
                print(f"The route \"{self.route}\" you provided does not appear in the default available routes.\n")
            return False
        if not isinstance(self.frequency, str) and self.frequency is not None:
            raise TypeError("The frequency variable should be a string type.\n")
        if 'frequency' not in layer:
            if self.verbose >= 0:
                print("Warning: You have provided a partial route. You will be able to print route information with the route_endpoints function or by printing the class instance.\n")
            return False
        if 'data' in layer:
            for item in self.data:
                if item not in layer['data']:
                    if self.verbose >= 0:
                        print("Warning: One or more of your data variables does not appear to be in the default route.\n")
                    return False
        if 'facets' in layer:
            single = self.check_list_single(self.facets)
            if single:
                return False
            else:
                for item in self.facets:
                    try:
                        tmp_bool = item[0] not in layer['facets'] or item[1] not in layer['facets'][item[0]]
                    except:
                        if self.verbose >= 0:
                            print("Warning: One of your facet_types variables is not in the default route. Should be formatted [(facet_type0, facet_id0), (facet_type1, facet_id1),...].\nFor more information about possible default facet ids related to a given facet type you can run the route_endpoints() function while passing a string to the facet_types instance variable.\n")
                        return False
                    if tmp_bool:
                        if self.verbose >= 0:
                            print("Warning: One of your facet_types variables is not in the default route. Should be formatted [(facet_type0, facet_id0), (facet_type1, facet_id1),...].\nFor more information about possible default facet ids related to a given facet type you can run the route_endpoints() function while passing a string to the facet_types instance variable.\n")
                        return False
        if 'sort_by' in layer:       
            for item in self.sort:
                if item[0] not in layer or item[1] not in ['asc', 'desc']:
                    if self.verbose >= 0:
                        print("Warning: One of your sort variable does not appear to be in the default route. Or one of your sort directions does not appear to be 'asc' or 'desc'.\n")
                    return False
        return True
    
    
    
    def route_info(self):
        base_url = 'https://api.eia.gov/v2/'
        base_url += self.route + '/'
        
        if self.check_list_single(self.facets):
            base_url += f'facet/{self.facets[0]}'
        base_url += '?'
        response = get_post(base_url, api_key=self.api_key, verbose=self.verbose)
        return response
    def update_tree(self):
        route_tree = {}
        short_route_tree = {}
        stack = []
        
        for item in self.get_api_layer()['response']['routes']:
            stack.append([item['id']])
            route_tree[item['id']] = {}
            short_route_tree[item['id']] = {}
        
        while len(stack)>0:
            
            current_route = stack.pop()
            if self.verbose >= 2:
                print(f"Stack length: {len(stack)}")
            str_route = '/'.join(current_route)
            start_time = time.time()
            layer = self.get_api_layer(route=str_route)['response']
            tts = self.sleep_between_calls - (time.time()-start_time)
            if tts < 0:
                tts = 0
            time.sleep(tts)
            if 'frequency' in layer:
                bottom_dict = self.search_nested_dict(current_route, route_tree)
                bottom_dict['frequency'] = [item['id'] for item in layer['frequency']]
                bottom_dict['data'] = [item for item in layer['data']]
                fac_dict = {}
                for f in layer['facets']:
                    fac_dict[f['id']] = [item['id'] for item in self.get_api_layer(route=str_route, facet=f['id'])['response']['facets']]
                bottom_dict['facets'] = fac_dict
                bottom_dict['sort_by'] = ['period'] + list(bottom_dict['facets'].keys()) + bottom_dict['data']

                short_bottom_dict = self.search_nested_dict(current_route, short_route_tree)
            
                short_bottom_dict['facets'] = {key: bottom_dict['facets'][key][:5] + (['...'] if len(bottom_dict['facets'][key]) > 5 else []) 
                                               for key in bottom_dict['facets']}
                                               
                short_bottom_dict['frequency'] = [x for x in bottom_dict['frequency'][:5]] + (['...'] if len(bottom_dict['frequency']) > 5 else [])
                short_bottom_dict['data'] = [x for x in bottom_dict['data'][:5]] + (['...'] if len(bottom_dict['data']) > 5 else [])
                short_bottom_dict['sort_by'] = [x for x in bottom_dict['sort_by'][:5]] + (['...'] if len(bottom_dict['sort_by']) > 5 else [])
        

            else:
                for item in layer['routes']:
                    self.search_nested_dict(current_route, route_tree)[item['id']] = {}
                    current_copy = list(current_route)
                    current_copy.append(item['id'])
                    stack.append(current_copy)

                    self.search_nested_dict(current_route, short_route_tree)[item['id']] = {}
                    
        with open("updated_route_tree.json", 'w') as f:
            json.dump(route_tree, f, indent=2)
        with open("updated_short_route_tree.json", 'w') as f:
            json.dump(short_route_tree, f, indent=2)

    #Disabled if facet is singular
    def check_enabled(self):
        if not self.enable_functions:
            raise TypeError("The function you requested is not enabled because of missing information or incorrectly formatted information. To override set the override instance variable to True.")
        
    def url_constructor(self, start, end):
        base_url = 'https://api.eia.gov/v2/'
        base_url += self.route
        base_url += '/data/?'
        if self.frequency:
            base_url += "frequency=" + self.frequency
        for d in range(len(self.data)):
            dat = self.data[d]
            base_url +=  f'&data[{d}]=' + dat
        for facet, facet_id in self.facets:
            base_url += f"&facets[{facet}][]={facet_id}"
        if start: 
            base_url += f"&start={start}T00&"
        if end:
            base_url += f"end={end}T00&"
        
        for s_id, s_dir in self.sort:
                base_url += f'sort[0][column]={s_id}&sort[0][direction]={s_dir}&'
        base_url += f'offset=0&length=5000'
        return base_url
    

    def request_data(self, start, end, as_df=True):
        self.check_enabled()
        url = self.url_constructor(start, end)
        response = get_post(url, self.api_key, self.verbose)
        if 'warnings' in response['response'] and self.verbose >= 0:
            print(f"API WARNING: The following warning comes from a request made from {start} to {end}\n")
            print(json.dumps(response['response']['warnings'], indent=2))
        
        if as_df:
            try:
                df = resp2df(response)
                return df
            except:
                if self.verbose >= 1:
                    print(f'No output for this period: \nStart Date: {start}\nEnd Date: {end}\n')
                return None
        else:
            return response
    def request_data_as_df(self, start, end):
        return self.request_data(start, end, as_df=True)
    
    def request_raw_data(self, start, end):
        return self.request_data(start, end, as_df=False)
    
    def collect_month_of_small_data(self, year, month):
        to_return = []
        dates = split_month_dates(year, month, month_multiplier=self.multiplier)
        for date in dates:
            if self.verbose >= 1:
                print(f'Collecting from {date[0]} to {date[1]}')
            start_time = time.time()
            df = self.request_data_as_df(date[0], date[1])
            tts = self.sleep_between_calls - (time.time()-start_time)
            if tts < 0:
                tts = 0
            time.sleep(tts)
            if df is not None:
                to_return.append(df)
        return to_return
    

    def collect_year_small_data(self, year, engine, months=None):
        if months is None:
            months=range(1,13)
        
        dfs = []
       
        for month in months:
            for item in self.collect_month_of_small_data(year, month):
                dfs.append(item)
           
            
        if dfs:
            df = pd.concat(dfs, axis=0)
            df.drop_duplicates(inplace=True)
            
            if self.write2db:
                df.to_sql(self.tablename, engine, index=False, if_exists='append')
            if self.yield_df:
                yield df
    def collect_months_of_large(self, dates):
        if self.verbose >= 1:
                print(f'Collecting from {dates[0]} to {dates[1]}')
        start_time = time.time()
        df = self.request_data_as_df(dates[0], dates[1])
        tts = self.sleep_between_calls - (time.time()-start_time)
        if tts < 0:
            tts = 0
        time.sleep(tts)
        return df
        


    def collect_year_large_data(self, the_range, engine):
        date_ranges = []
        if self.multiplier >= 1:
            date_ranges = generate_date_ranges(the_range[0], the_range[len(the_range)-1], self.multiplier)
        else:
            for year in the_range:
                for month in range(1,13):
                    date_ranges += split_month_dates(year=year, month=month, month_multiplier=self.multiplier)
        
        dfs = []
      
        for date_ in date_ranges:
            tmp_df = self.collect_months_of_large(date_)
                           
            dfs.append(tmp_df)
            
        df = pd.concat(dfs, axis=0)
        df.drop_duplicates(inplace=True)
        if self.write2db:
            df.to_sql(self.tablename, engine, index=False, if_exists='append')
        if self.yield_df:
            yield df
        
    def collect_years_data(self, years=None, start_year=None, end_year=None):
        if (start_year and not end_year) or (end_year and not start_year):
            raise ValueError("You either provided a start_year and no end_year or a end_year and no start_year.")
        if years and not check_iterable(years):
            raise TypeError("The 'years' variable must be an iterable object, such as a list or tuple.")
        if not years and (not start_year or not end_year):
            raise ValueError("Not enough information provided for years you would like to collect information on. If you would like to collect information on multiple years, please provide an iterable with the years you would like to collect information on through the \'years\' variable. Alternetavely provide a range through the \'start_year\' and \'end_year\' variables.")
        engine = None
        if self.write2db:
            engine = self.start_engine()
        
        if years is None:
            years = range(start_year, end_year+1)
        else:
            years = sorted(years)
        if self.yield_df and ("hourly" in self.frequency or 'week' in self.frequency or 'daily' in self.frequency):
            for y in years:                    
                for df in self.collect_year_small_data(y, engine):
                        yield df
        elif "hourly" in self.frequency or 'week' in self.frequency or 'daily' in self.frequency:  
            for y in years:                    
                self.collect_year_small_data(y, engine)
                               
        elif self.yield_df and ('monthly' in self.frequency or 'quarterly' in self.frequency or 'yearly' in self.frequency) and (len(years) == 1 or all(years[i + 1] - years[i] == 1 for i in range(len(years) - 1))):
                for df in self.collect_year_large_data(years, engine):
                    yield df

        elif ('monthly' in self.frequency or 'quarterly' in self.frequency or 'yearly' in self.frequency) and (len(years) == 1 or all(years[i + 1] - years[i] == 1 for i in range(len(years) - 1))):
                self.collect_year_large_data(years, engine)

        elif self.yield_df and ('monthly' in self.frequency or 'quarterly' in self.frequency or 'yearly' in self.frequency):
                for y in years:
                    self.collect_year_large_data([y], engine)

        elif 'monthly' in self.frequency or 'quarterly' in self.frequency or 'yearly' in self.frequency:
            for y in years:
                    self.collect_year_large_data([y], engine)
        elif self.large_granularity and self.yield_df:
            yield self.collect_year_large_data(years, engine)
        elif self.large_granularity:
            self.collect_year_large_data(years, engine)
        elif self.yield_df:
            if self.verbose > 0:
                print("Warning: The frequency you provided is not on the default route. Default behavior will be to collect as though you provided a \nfrequency of smaller granularity, to use larger granularity you can set large_granularity to True.\n")
            for y in years:
                yield self.collect_year_small_data([y], engine)
        else:   
            if self.verbose > 0:
                print("Warning: The frequency you provided is not on the default route. Default behavior will be to collect as though you provided a \nfrequency of smaller granularity, to use larger granularity you can set large_granularity to True.\n")
            for y in years:
                self.collect_year_small_data([y], engine)
        if self.write2db:       
            engine.dispose()
    def start_engine(self):
        if self.pwd is not None:
            return create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=self.host, db=self.dbname, user=self.username, pw=self.pwd))
        else:
            return create_engine("mysql+pymysql://{user}@{host}/{db}".format(host=self.host, db=self.dbname, user=self.username))

            
    def collect_months_data(self, year, months=None, start_month=None, end_month=None):
        if (start_month and not end_month) or (end_month and not start_month):
            raise ValueError("You either provided a start_month and no end_month or a end_month and no start_month.")
        if months and not check_iterable(months):
            raise TypeError("The 'months' variable must be an iterable object, such as a list or tuple.")
        if not months and (not start_month or not end_month):
            raise ValueError("Not enough information provided for months you would like to collect information on. If you would like to collect information on multiple months, please provide an iterable with the months you would like to collect information on through the \'months\' variable. Alternetavely provide a range through the \'start_month\' and \'end_month\' variables.")
        engine = None
        if self.write2db:
            engine = self.start_engine()
        
        if months is None:
            months = range(start_month, end_month+1)
  
        if "hourly" in self.frequency and self.yield_df:
            for df in self.collect_year_small_data(year, engine, months=months):
                    yield df
        else:
            self.collect_year_small_data(year, engine, months=months)

        if 'monthly' in self.frequency or 'quarterly' in self.frequency or 'yearly' in self.frequency and self.yield_df:
            for df in self.collect_year_large_data([year], engine):
                    yield df
        else:
            self.collect_year_large_data([year], engine)
            
        if self.write2db:       
            engine.dispose()
    def search_nested_dict(self, keys, nested_dict):
        """
        Traverses a nested dictionary using a list of keys.
        
        :param keys: List of keys to traverse the dictionary.
        :param nested_dict: The dictionary to search through.
        :return: The value found after traversing the dictionary, or raises KeyError if a key is missing.
        """
        current_level = nested_dict  # Start at the top level of the dictionary
        for key in keys:
            if isinstance(current_level, dict) and key in current_level:
                current_level = current_level[key]  # Move one level deeper
            else:
                raise KeyError(f"Key '{key}' not found in the dictionary at the current level.")
        return current_level
    def get_api_layer(self, route=None, facet=None):
        base_url = 'https://api.eia.gov/v2/'
        if route is not None:
            base_url += route + '/'
        
        if facet is not None:
            base_url += f'facet/{facet}'
        base_url += '?'
        response = get_post(base_url, api_key=self.api_key, verbose=self.verbose)
        return response
    
  

    


