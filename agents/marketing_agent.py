import os


class MarketingAgent:

    def generate(self, book):

        print("\n📢 Marketing Agent Running...\n")

        title = book["title"]
        subtitle = book["subtitle"]

        pinterest = f"{title} | {subtitle}"

        instagram = f"""
🎨 {title}

{subtitle}

Perfect for kids ages 4-8.

#coloringbook #kidscoloring #amazonkdp #activitybook #animals
"""

        facebook = f"""
NEW RELEASE!

{title}

{subtitle}

40 fun coloring pages for kids.
Perfect gift for boys and girls.
"""

        hashtags = """
#coloringbook
#kidscoloring
#animalcoloring
#amazonkdp
#activitybook
#homeschool
#preschool
"""

        os.makedirs("output/marketing", exist_ok=True)

        with open("output/marketing/pinterest.txt", "w") as f:
            f.write(pinterest)

        with open("output/marketing/instagram.txt", "w") as f:
            f.write(instagram)

        with open("output/marketing/facebook.txt", "w") as f:
            f.write(facebook)

        with open("output/marketing/hashtags.txt", "w") as f:
            f.write(hashtags)

        print("✅ Marketing files created.")

        return {
            "pinterest": pinterest,
            "instagram": instagram,
            "facebook": facebook
        }