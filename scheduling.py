from sqlalchemy import create_engine, Column, Integer, Date, VARCHAR   # import used types
from sqlalchemy.orm import declarative_base, sessionmaker

import os   #clear screen

from utils import fanymodules as fm    # my own "lib"

from datetime import datetime, timedelta    # import day and hour

from tabulate import tabulate   # print a beautiful table

from colorama import init, Fore, Style    # colors
init()


DATABASE_URL = # postgresql+psycopg2://usuario:senha@localhost:5432/your_database


engine = create_engine(DATABASE_URL)   # connect with the database
Session = sessionmaker(bind=engine)
Base = declarative_base()



#------------------- MENU -------------------


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')    #clear screen
    
    
def menu_choice():
    clear_screen()
    print(f'{Fore.RED}============= M E N U ============={Style.RESET_ALL}')
    print('0 - Finish program')
    print('1 - Schedule appointment')
    print('2 - Cancel appointment')
    print('3 - Register concluded appointment')
    print('4 - Check alerts')
    print('5 - Check tables per period')
    
    
    choice = fm.input_choice(
                    msg = 'Choose an option between 0 - 5: ',
                    valid_options = (0, 1, 2, 3, 4, 5),
                    error_msg = 'invalid option.',
                    use_color = True
    )
    return choice
    
    
    
#------------------- CLASSES -------------------



class AppointmentsTable(Base):   # class is mandatory with database
    __tablename__ = 'appointments'   # creating table appointments
    id = Column(Integer, primary_key=True)
    appointment = Column(VARCHAR)
    date = Column(Date)
    note = Column(VARCHAR)  # observation
    
    
    
class CanceledTable(Base):   # class is mandatory with database
    __tablename__ = 'canceled'   # creating table canceled
    id = Column(Integer, primary_key=True)
    appointment = Column(VARCHAR)
    date = Column(Date)
    cancel_reason = Column(VARCHAR)
    
    

class ConcludedTable(Base):   # class is mandatory with database
    __tablename__ = 'concluded'   # creating table concluded
    id = Column(Integer, primary_key=True)
    appointment = Column(VARCHAR)
    concluded_date = Column(Date)
    note = Column(VARCHAR)
    
    
Base.metadata.create_all(engine) # create all tables in database


#------------------- FUNÇÕES -------------------




def option_1():  # Schedule appointment
    while True:
        
        appointment = fm.input_non_empty(
                msg = 'enter the appointment here: ',
                error_msg = 'invalid appointment',
                case = 'title',
                use_color = True
        )
        


        # taking date
        date = fm.input_date(
                msg = 'enter the date: ',
                error_msg = 'invalid date. Use DD/MM/YYYY',
                use_color = True
        )



        with Session() as session:  #create session

            existing_appointment = session.query(AppointmentsTable).filter_by(     # verify if product already exists using the variables below
                    appointment=appointment,
                    date=date,
                ).first()

            if existing_appointment:    # if appointment already exist
                print(f'{Fore.YELLOW}appointment already exist!{Style.RESET_ALL}')
                continue
                    
            else:     
                    note = fm.get_confirm(
                        msg = 'Do you want to enter a observation? (yes/no): ',
                        yes = 'yes',
                        no = 'no',
                        error_msg = 'Insert a valid option',
                        use_color = True
                    )  # observation validation
                                
                    if note:
                        note = fm.input_non_empty(
                            msg = 'enter the observation here: ',
                            error_msg = 'invalid observation',
                            case = 'title',
                            use_color = True
                    )
                            
                    else:
                        note = None

                        
            try:
                new_record = AppointmentsTable(appointment = appointment, date = date,
                                                        note = note)
                                    
                session.add(new_record)
                session.commit()     # enter in PostgreSQL
                print(f'{Fore.GREEN}The new appointment was registered!{Style.RESET_ALL}')
                                
            except Exception as error:
                session.rollback()
                print(f'{Fore.RED}ERROR: {error}{Style.RESET_ALL}')
                        
                        
            if not fm.get_confirm(
                            msg = 'do you want to repeat? (yes/no): ',
                            yes = 'yes',
                            no = 'no',
                            error_msg = 'Invalid option.', 
                            use_color = True):   # verify if the program will repeat or no
                break
                    
        
        
        
def option_2(): # cancel appointment
    while True:
        
        appointment = fm.input_non_empty(
                msg = 'enter the appointment here: ',
                error_msg = 'invalid appointment',
                case = 'title',
                use_color = True
        )


        date = fm.input_date(
                msg = 'Enter the scheduled date: ',
                error_msg = 'invalid date. Use DD/MM/YYYY',
                use_color = True
        )
        
        

        with Session() as session:  #create session


            # search item in table appointments
            appointment_item = session.query(AppointmentsTable).filter_by(
                appointment=appointment,
                date=date
                ).first()


            # check if exist
            if not appointment_item:
                print(f'{Fore.RED}ERROR: {appointment} to date: {date} doesnt exist.{Style.RESET_ALL}')

                if not fm.get_confirm(
                    msg = 'do you want to repeat? (yes/no): ',
                    yes = 'yes',
                    no = 'no',
                    error_msg = 'Insert a valid option',
                    use_color = True):   # verify if the program will repeat or no
                    break
                else:
                    continue


            cancel_reason = fm.input_non_empty(
                            msg = 'enter the cancel reason here: ',
                            error_msg = 'invalid cancel reason',
                            case = 'title',
                            use_color = True
                )
            
            
            try:
                new_record = CanceledTable(appointment=appointment, date=date, cancel_reason=cancel_reason)
                
                session.add(new_record)
                session.delete(appointment_item)    # delete item of table appointments
                session.commit()    # enter in PostgreSQL
                print(f'{Fore.GREEN}Delete completed!{Style.RESET_ALL}')
            except Exception as error:
                session.rollback()
                print(f'{Fore.RED}ERROR: {error}{Style.RESET_ALL}')


        if not fm.get_confirm(
                    msg = 'do you want to repeat? (yes/no): ',
                    yes = 'yes',
                    no = 'no',
                    error_msg = 'Invalid option.',
                    use_color = True):   # verify if the program will repeat or no
                    break
        
        
        
        
def option_3(): # concluded appointment
    while True:
        
        appointment = fm.input_non_empty(
            msg = 'enter the appointment here: ',
            error_msg = 'invalid appointment',
            case = 'title',
            use_color = True
        )


        date = fm.input_date(
                msg = 'enter the appointment date: ',
                error_msg = 'invalid date. Use DD/MM/YYYY',
                use_color = True
        )
        


        with Session() as session:  #create session


            # search item in table appointments
            appointment_item = session.query(AppointmentsTable).filter_by(
                appointment=appointment,
                date=date
                ).first()


            # check if exist
            if not appointment_item:
                print(f'{Fore.RED}ERROR: {appointment} to date: {date} doesnt exist.{Style.RESET_ALL}')

                if not fm.get_confirm(
                    msg = 'do you want to repeat? (yes/no): ',
                    yes = 'yes',
                    no = 'no',
                    error_msg = 'Insert a valid option',
                    use_color = True):   # verify if the program will repeat or no
                    break
                else:
                    continue



            concluded_date = fm.input_date(
                        msg = 'enter the concluded appointment date: ',
                        error_msg = 'Invalid date. Use DD/MM/YYYY',
                        use_color = True)
            
            
            
            note = fm.get_confirm(
                            msg = 'Do you want to enter a observation? (yes/no): ',
                            yes = 'yes',
                            no = 'no',
                            error_msg = 'Insert a valid option',
                            use_color = True
            )  # observation validation
             
            if note:
                note = fm.input_non_empty(
                msg = 'enter the observation here: ',
                error_msg = 'invalid observation',
                case = 'title',
                use_color = True
                )
            else:
                note = None
            
            
            
            try:
                new_record = ConcludedTable(appointment=appointment, concluded_date=concluded_date, note=note)
                
                session.add(new_record)
                session.delete(appointment_item)    # delete item of table appointments
                session.commit()    # enter in PostgreSQL
                print(f'{Fore.GREEN}all completed!{Style.RESET_ALL}')
            except Exception as error:
                session.rollback()
                print(f'{Fore.RED}ERROR: {error}{Style.RESET_ALL}')


        if not fm.get_confirm(
                    msg = 'do you want to repeat? (yes/no): ',
                    yes = 'yes',
                    no = 'no',
                    error_msg = 'Invalid option.', 
                    use_color = True):   # verify if the program will repeat or no
                    break
        
        
        
        
def option_4():  # alerts for upcoming appointments
    
    with Session() as session:
            
        today = datetime.now().date()
        limit_date = today + timedelta(days=7)  # date period limit with timedelta


        alerts = session.query(AppointmentsTable).filter(
            AppointmentsTable.date >= today,
            AppointmentsTable.date <= limit_date
        ).order_by(AppointmentsTable.date).all()


        if alerts:
            print(f'\n{Fore.CYAN}============= ALERTS ============={Style.RESET_ALL}')
            print(f'From {today} to {limit_date}')
            print()

            for i in alerts:
                print(f'{Fore.YELLOW}{i.appointment} scheduled for {i.date} | Note: {i.note}{Style.RESET_ALL}')

        else:
            print(f'\n{Fore.WHITE}No appointments in the next 7 days.{Style.RESET_ALL}')
            
            
        
        
def option_5():   # check tables
    while True:
        
        table_choice = fm.input_choice(
                    msg = 'Which table would you like to view | (1) appointments | (2) canceled | (3) concluded |: ',
                    valid_options = (1, 2, 3),
                    error_msg = 'enter a valid option',
                    use_color = True
        )
                
                
        with Session() as session:  # create session
                
                
            # table choice
            if table_choice == 1:
                table_class = AppointmentsTable 
            elif table_choice == 2:
                table_class = CanceledTable
            else:
                table_class = ConcludedTable
                    
                    
            # taking start date
            start_date, end_date = fm.input_date_range(
                                                    start_msg = 'Start date (DD/MM/YYYY): ',
                                                    end_msg = 'End date (DD/MM/YYYY): ',
                                                    format_error_msg = 'Invalid date. Use DD/MM/YYYY.',
                                                    range_error_msg = 'End date must be after start date.',
                                                    use_color = True
                                                )
                    
        
            if table_class == CanceledTable or table_class == AppointmentsTable:
                records_period = session.query(table_class).filter(
                    table_class.date >= start_date,
                    table_class.date <= end_date
                    ).order_by(table_class.date).all()
                
            else:
                records_period = session.query(table_class).filter(
                    table_class.concluded_date >= start_date,
                    table_class.concluded_date <= end_date
                    ).order_by(table_class.concluded_date).all()
                
                
                
            if not records_period:
                print(f'\n{Fore.YELLOW}Nothing registered in the table {table_class.__tablename__} in this period!{Style.RESET_ALL}')
                if not fm.get_confirm(
                    msg = 'do you want to repeat? (yes/no): ',
                    yes = 'yes',
                    no = 'no',
                    error_msg = 'Insert a valid option',
                    use_color = True):   # verify if the program will repeat or no
                    continue
                else:
                    return

            print(f'\n{Fore.CYAN}================== TABELA {table_class.__tablename__.upper()} =================={Style.RESET_ALL}')
            print(f'{start_date} <-----> {end_date}')
                
                
            # take Columns name
            columns = table_class.__table__.columns.keys()  # __table__ is a entire table in SQLAlchemy and columns.keys() return a list with columns name
                
                
            # create data list
            table_data = []


            for r in records_period:
                row = []  # create empty list

                for col in columns:  # go through each column name
                    value = getattr(r, col)  # get the value of that column
                    row.append(value)  # add the value to the row
                        
                table_data.append(row)  # add the row to the table data

            # showing the table
            print(tabulate(table_data, headers=columns, tablefmt="fancy_grid"))
        
        
        if not fm.get_confirm(
                    msg = 'do you want to repeat? (yes/no): ',
                    yes = 'yes',
                    no = 'no',
                    error_msg = 'Invalid option.', 
                    use_color = True):   # verify if the program will repeat or no
                    break
        
        
        
        
#------------------- MAIN LOOP -------------------

while True:
    
    choice = menu_choice()

    if choice == 1:   # Schedule appointment
        option_1()

    elif choice == 2:   # Cancel appointment 
        option_2()

    elif choice == 3:   # Concluded appointment
        option_3()
        
    elif choice == 4:   # check alerts
        option_4()
    
    elif choice == 5:   # check Tables
        option_5()
    
    else:
        print(f'\n{Fore.WHITE}======= FINISHED PROGRAM ======={Style.RESET_ALL}')
        break


    if not fm.get_confirm(
        msg = 'Do you want to return to the Menu? (yes/no): ',
        yes = 'yes',
        no = 'no',
        error_msg = 'Invalid option.', 
        use_color = True):
        print(f'\n{Fore.WHITE}======= FINISHED PROGRAM ======={Style.RESET_ALL}')
        break
