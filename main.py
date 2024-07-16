# -*- coding: utf-8 -*-

from classes.LDscrapper import LinkedinDriver

def main():
    ldriver = LinkedinDriver("relaxingscript@gmail.com", "testtest123")
    try:
        ldriver.login()
        ldriver.search_easy_apply_jobs()
        ldriver.collect_jobs(pages=2)  # Indica cuántas páginas deseas navegar
        for i, title in enumerate(ldriver.job_titles):
            print(f"Job {i+1}: {title}\n")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        ldriver.close()

if __name__ == "__main__":
    main()