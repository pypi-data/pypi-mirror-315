import instaloader

class InstagramInfo:
    def __init__(self, username):
        self.username = username
        self.loader = instaloader.Instaloader()

    def get_profile_info(self):
        """Lấy thông tin hồ sơ của người dùng Instagram"""
        profile = instaloader.Profile.from_username(self.loader.context, self.username)
        profile_info = {
            'username': profile.username,
            'full_name': profile.full_name,
            'bio': profile.biography,
            'followers': profile.followers,
            'following': profile.followees,
            'posts': profile.mediacount,
            'is_verified': profile.is_verified
        }
        return profile_info
        