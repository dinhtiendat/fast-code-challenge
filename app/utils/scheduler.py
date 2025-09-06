import uuid
import datetime
from sqlalchemy.orm import Session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.repository.match import MatchRepository
from app.repository.history import HistoryRepository
from app.repository.ah_data import AHDataRepository
from app.repository.ou_data import OUDataRepository
from app.models.history import History
from app.models.ah_data import AHData
from app.models.ou_data import OUData
from app.db.session import SessionLocal


def scrape():
    def mapping_ah_data(_ah_data, _history_id):
        now = datetime.datetime.utcnow()
        return [AHData(
            id=str(uuid.uuid4()),
            history_id=_history_id,
            order=record[0],
            ah_value=record[1],
            odds1=record[2],
            odds2=record[3],
            payout=record[4],
            created_at=now,
        ) for record in _ah_data]

    def mapping_ou_data(_ou_data, _history_id):
        now = datetime.datetime.utcnow()
        return [OUData(
            id=str(uuid.uuid4()),
            history_id=_history_id,
            order=record[0],
            ou_value=record[1],
            odds1=record[2],
            odds2=record[3],
            payout=record[4],
            created_at=now,
        ) for record in _ou_data]

    db: Session = SessionLocal()
    repo_match = MatchRepository(db)
    repo_history = HistoryRepository(db)
    repo_ah_data = AHDataRepository(db)
    repo_ou_data = OUDataRepository(db)
    matches = repo_match.get_all()
    if len(matches) > 0:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        error_cookies, source_page_cookies = click_cookies(driver)

        for match in matches:
            start_time = datetime.datetime.utcnow()
            status, ah_data, ou_data, error_decimal_odds, error_ah, error_ou, source_page_decimal_odds, source_page_ah, source_page_ou = scrape_data(driver, match)
            end_time = datetime.datetime.utcnow()

            duration = round((end_time - start_time).total_seconds(), 1)

            history_id = str(uuid.uuid4())
            history = History(
                id=history_id,
                match_id=match.id,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                status=status,
                error_cookies=error_cookies,
                error_decimal_odds=error_decimal_odds,
                error_ah=error_ah,
                error_ou=error_ou,
                source_page_cookies=source_page_cookies,
                source_page_decimal_odds=source_page_decimal_odds,
                source_page_ah=source_page_ah,
                source_page_ou=source_page_ou,
                created_at=datetime.datetime.utcnow()
            )
            repo_history.create(history)

            if (ah_data is not None) and (len(ah_data) > 0):
                repo_ah_data.create_many(mapping_ah_data(ah_data, history_id))
            if (ou_data is not None) and (len(ou_data) > 0):
                repo_ou_data.create_many(mapping_ou_data(ou_data, history_id))


def scrape_data(driver, match):
    driver.set_window_size(1200, 2000)

    driver.get(match.match_url)
    print(driver.current_url)

    driver.execute_script("window.scrollBy(0, -10000);")
    error_decimal_odds, source_page_decimal_odds = click_decimal_odds(driver)

    ah_data, error_ah, source_page_ah = get_ah_table(driver)
    ou_data, error_ou, source_page_ou = get_ou_table(driver)
    if (ah_data is not None) and (ou_data is not None) and (len(ah_data) > 0) and (len(ou_data) > 0):
        return True, ah_data, ou_data, error_decimal_odds, error_ah, error_ou, source_page_decimal_odds, source_page_ah, source_page_ou
    else:
        return False, ah_data, ou_data, error_decimal_odds, error_ah, error_ou, source_page_decimal_odds, source_page_ah, source_page_ou


def click_cookies(driver):
    error = ""
    source_page = ""
    url = "https://www.oddsportal.com/"
    driver.get(url)

    try:
        element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
        )
        element.click()
    except Exception as e:
        print(datetime.datetime.utcnow().strftime("%Y-%d-%m %H:%M:%S"), " click_cookies: ", e)
        error = str(e)
        source_page = str(driver.find_element(By.XPATH, "//body").get_attribute("innerHTML"))
    return error, source_page


def click_decimal_odds(driver):
    error = ""
    source_page = ""
    try:
        driver.find_element(By.XPATH, "//p[contains(text(),'Odds formats')]/../../div[2]").click()
        decimal_odds = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//p[contains(text(),'Odds formats')]/../../div[2]/div[contains(@class, 'dropdown-content')]/ul/li/a/span[contains(text(), 'Decimal Odds (1.50)')]/.."))
        )
        decimal_odds.click()
    except Exception as e:
        print(datetime.datetime.utcnow().strftime("%Y-%d-%m %H:%M:%S"), " click_decimal_odds: ", e)
        error = str(e)
        source_page = str(driver.find_element(By.XPATH, "//body").get_attribute("innerHTML"))
    return error, source_page


def get_ah_table(driver):
    ah_data = []
    error = ""
    source_page = ""
    try:
        driver.find_element(By.XPATH, "//li/span/div[contains(text(),'Asian Handicap')]").click()

        table_data = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[contains(text(), 'Payout')]/../../../div[not(contains(@class,'flex-col'))]"))
        )
        rows = table_data.find_elements(By.XPATH, "//div[contains(@class, 'flex-col')][contains(@set, '0')]")
        idx = 1
        for row in rows:
            ah_value = row.find_element(By.CSS_SELECTOR,
                                        "div.border-black-borders.cursor-pointer > div:nth-child(2) > p").text
            odds1 = row.find_element(By.CSS_SELECTOR,
                                     "div.border-black-borders.cursor-pointer > div:nth-child(3) > div:nth-child(1)").text
            odds2 = row.find_element(By.CSS_SELECTOR,
                                     "div.border-black-borders.cursor-pointer > div:nth-child(3) > div:nth-child(2)").text
            payout = row.find_element(By.CSS_SELECTOR,
                                      "div.border-black-borders.cursor-pointer > div:nth-child(3) > div:nth-child(3)").text
            ah_data.append([idx, ah_value, odds1, odds2, payout])
            idx += 1
    except Exception as e:
        print(datetime.datetime.utcnow().strftime("%Y-%d-%m %H:%M:%S"), " get_ah_table: ", e)
        error = str(e)
        source_page = str(driver.find_element(By.XPATH, "//body").get_attribute("innerHTML"))
    return ah_data, error, source_page


def get_ou_table(driver):
    ou_data = []
    error = ""
    source_page = ""
    try:
        driver.find_element(By.XPATH, "//li/span/div[contains(text(),'Over/Under')]").click()

        table_data = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[contains(text(), 'Payout')]/../../../div[not(contains(@class,'flex-col'))]"))
        )
        rows = table_data.find_elements(By.XPATH, "//div[contains(@class, 'flex-col')][contains(@set, '0')]")
        idx = 1
        for row in rows:
            ou_value = row.find_element(By.CSS_SELECTOR,
                                        "div.border-black-borders.cursor-pointer > div:nth-child(2) > p").text
            odds1 = row.find_element(By.CSS_SELECTOR,
                                     "div.border-black-borders.cursor-pointer > div:nth-child(3) > div:nth-child(1)").text
            odds2 = row.find_element(By.CSS_SELECTOR,
                                     "div.border-black-borders.cursor-pointer > div:nth-child(3) > div:nth-child(2)").text
            payout = row.find_element(By.CSS_SELECTOR,
                                      "div.border-black-borders.cursor-pointer > div:nth-child(3) > div:nth-child(3)").text
            ou_data.append([idx, ou_value, odds1, odds2, payout])
            idx += 1
    except Exception as e:
        print(datetime.datetime.utcnow().strftime("%Y-%d-%m %H:%M:%S"), " get_ou_table: ", e)
        error = str(e)
        source_page = str(driver.find_element(By.XPATH, "//body").get_attribute("innerHTML"))
    return ou_data, error, source_page
