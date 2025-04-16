from playwright.sync_api import Playwright, sync_playwright, expect
from mdutils import MdUtils
from pathlib import Path
import time

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={ 'width': 1920, 'height': 968 })
    page = context.new_page()

    page.goto("https://www.google.fr/maps")
    if page.get_by_role("button", name="Tout refuser").is_visible():
        page.get_by_role("button", name="Tout refuser").click()
    page.wait_for_load_state('domcontentloaded')
    
    mdFile = MdUtils(file_name='Parcours',
                     title="Parcours duathlon: points d'attention")


    # Open the file in read mode
    with open('parcours_velo_streetview.txt', 'r') as file, open('parcours_velo_satellite.txt', 'r') as file_sat:
        # Read each line in the file
        i = 1
        for line in file:
            # Print each line
            url = line.strip()
            url_sat = file_sat.readline()
            image_path = f"./{i}.jpg"
            image_path_sat = f"./{i}_sat.jpg"
            page.goto(url, wait_until='networkidle')
            title = page.title()
            if not Path(image_path).is_file() :
                page.screenshot(path=image_path)
                print(f"save image {i}")
            if not Path(image_path_sat).is_file() and url_sat :
                page.goto(url_sat, wait_until='networkidle')
                page.get_by_title("Fermer").click()
                time.sleep(2)
                page.locator("#legendPanel").get_by_role("button").nth(2).click()
                time.sleep(2)
                page.get_by_text("Réduire la légende de la carte").click()
                time.sleep(2)
                page.screenshot(path=image_path_sat)
                print(f"save image sat {i}")
            text_image = f'point {i} : {title}'
            text_image_sat = f'{text_image} vu satellite'
            print(text_image)
            mdFile.new_line(mdFile.new_inline_link(url, 
                                                   mdFile.new_inline_image(
                                                       text=text_image,
                                                       path=image_path)))
            mdFile.new_line(mdFile.new_inline_link(url, 
                                                   mdFile.new_inline_image(
                                                       text=text_image_sat,
                                                       path=image_path_sat)))
            mdFile.new_line(mdFile.new_inline_link(url, text_image))
            mdFile.new_line(mdFile.new_inline_link(url, text_image_sat))
            i += 1

    # ---------------------
    context.close()
    browser.close()

    mdFile.create_md_file()


with sync_playwright() as playwright:
    run(playwright)

# pandoc Parcours.md --variable colorlinks=true -o parcours.pdf
