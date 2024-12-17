from ffxivicongetter.core import actions_by_job, fetch_icons, fetch_user_skills

if __name__ == "__main__":
    skills = fetch_user_skills()
    actions_by_job = actions_by_job(skills)

    print("Actions by job Done!")

    fetch_icons(actions_by_job)
