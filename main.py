import sys

from selenium_wrapper import SeleniumWrapper

import time, base64, os
import credentials




def website_automation(path_to_file, username, password, tags, page_title):
    # Initiate the driver
    if os.name == "posix":
        selenium_wrapper = SeleniumWrapper("https://doc.unifield.org/wp-admin/",
                                           geckodriver="resources/geckodriver_linux")
    else:
        selenium_wrapper = SeleniumWrapper("https://doc.unifield.org/wp-admin/",
                                           geckodriver="resources/geckodriver_win.exe")
    # Login page
    selenium_wrapper.find_element(("id", "user_login")).send_keys(username)
    selenium_wrapper.find_element(("id", "user_pass")).send_keys(password)
    selenium_wrapper.find_element(("id", "wp-submit")).click()
    # Click on posts in the navigation panel
    selenium_wrapper.find_element(("id", "menu-posts")).click()
    # Click on "Add new"
    selenium_wrapper.find_element(("xpath", "//div[@class='wrap']/a[text()='Add New']")).click()
    # Close the annoying prompt, but only if it actually appears
    popup = selenium_wrapper.find_element(("xpath", "//button[@aria-label='Close dialog']"), timeout=5,
                                          suppress_error=True)
    if popup is not None:
        popup.click()
    # Fill the page title
    selenium_wrapper.find_element(("id", "post-title-0")).send_keys(page_title)
    # Click on "Browse" to upload a document
    selenium_wrapper.find_element(("id", "mammoth-docx-upload")).send_keys(path_to_file)
    # Click on "Insert into Editor"
    selenium_wrapper.find_element(("id", "mammoth-docx-insert")).click()
    # Wait for the editor to fill
    selenium_wrapper.find_element(("xpath", "//div[@id='editor']//div[starts-with(@id, 'editor')]"),
                                  timeout=600)
    # Open the "Post" menu
    selenium_wrapper.find_element(("xpath", "//button[text()='Post']")).click()
    # Open the Categories harmonica
    selenium_wrapper.find_element(("xpath", "//button[text()='Categories']")).click()
    # Click on the right tags from the tag list
    for tag in tags:
        selenium_wrapper.find_element(("xpath", "//input[../../label[text()='{}']]".format(tag))).click()
    # Click on Publish (you need to click it once more to confirm)
    selenium_wrapper.find_element(("xpath", "//button[text()='Publish']")).click()
    selenium_wrapper.find_element(
        ("xpath", "//div[@class='editor-post-publish-panel']//button[text()='Publish']")).click()
    # Get the link
    link = selenium_wrapper.find_element(("id", "inspector-text-control-0")).get_attribute("value")
    # Safely close the browser
    selenium_wrapper.deinit()
    return link


def write_entry_to_file(filename, text):
    with open(filename, "a+") as file:
        file.write(text + "\n")


if __name__ == '__main__':
    user_username = credentials.username
    user_password = base64.b64decode(credentials.password_in_base64).decode('utf-8')
    tags = credentials.tags
    if "" in [user_username, user_password]:
        print("Please fill the credentials file with your username and password in base64")
        sys.exit()

    file_list = os.listdir("files_to_upload")
    file_list.sort()  # This is needed, so the files wouldn't upload in a random order
    for filename in file_list:
        if not filename.endswith(".docx") or filename.endswith(".doc"):
            continue
        path_to_file = os.path.join(os.getcwd(), "files_to_upload", filename)
        page_link = website_automation(path_to_file, user_username, user_password, tags,
                                       page_title=filename.split(".doc")[0],
                                       )

        entry = "{} {}".format(filename, page_link)
        write_entry_to_file(os.path.join("logs", "log.txt"), entry)
        write_entry_to_file(os.path.join("logs", "only_links.txt"), page_link)
        print(entry)
        time.sleep(1)  # A second of wait is needed because of wordpress timestamps
