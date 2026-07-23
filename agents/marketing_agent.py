import os


class MarketingAgent:

    def generate(self, book):

        print("\n📢 Marketing Agent Running...\n")

        title = book["title"]
        subtitle = book["subtitle"]

        # Derive a niche-specific hashtag from the book's actual
        # keyword/niche instead of hardcoding "#animals" for every
        # book regardless of subject (e.g. dinosaurs, space, etc.).
        niche_raw = book.get("keyword") or book.get("niche") or "coloring"
        niche_tag = "".join(ch for ch in niche_raw.lower().replace(" ", "") if ch.isalnum())
        niche_hashtag = f"#{niche_tag}coloring" if niche_tag else "#coloring"

        target_age = str(book.get("target_age") or "4-8").replace(" Years", "").replace("Years", "").strip()

        pinterest = f"{title} | {subtitle}"

        instagram = f"""
🎨 {title}

{subtitle}

Perfect for kids ages {target_age}.

#coloringbook #kidscoloring #amazonkdp #activitybook {niche_hashtag}
"""

        facebook = f"""
NEW RELEASE!

{title}

{subtitle}

{book.get('total_pages', book.get('pages', 40))} fun coloring pages for kids.
Perfect gift for boys and girls.
"""

        hashtags = f"""
#coloringbook
#kidscoloring
{niche_hashtag}
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