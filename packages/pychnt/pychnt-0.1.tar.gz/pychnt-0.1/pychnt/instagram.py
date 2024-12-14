import instaloader

class Instagram:
    def __init__(self):
        self.loader = instaloader.Instaloader()

    def get_profile_info(self, username):
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            info = {
                "username": profile.username,
                "full_name": profile.full_name,
                "bio": profile.biography,
                "followers": profile.followers,
                "following": profile.followees,
                "posts": profile.mediacount
            }
            return info
        except Exception as e:
            return {"error": str(e)}
