from django.shortcuts import render


# class RoleAccessMiddleware:
#     """
#     Middleware de contrôle d'accès basé sur les rôles
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         user = request.user
#         path = request.path

#         # 🚨 non connecté → on laisse Django gérer login/register
#         if not user.is_authenticated:
#             return self.get_response(request)

#         # =========================
#         # 🔐 ADMIN : accès total
#         # =========================
#         if user.role == "ADMIN":
#             return self.get_response(request)

#         # =========================
#         # 👮 AGENT
#         # =========================
#         if user.role == "AGENT":
#             allowed_prefixes = [
#                 "/agent/",
#                 "/results/",
#                 "/dashboard/",
#                 "/centers/",
#                 "/seats/",
#             ]

#             if any(path.startswith(p) for p in allowed_prefixes):
#                 return self.get_response(request)

#             return render(request, "core/access_denied.html")

#         # =========================
#         # 👤 ELECTEUR
#         # =========================
#         if user.role == "ELECTEUR":
#             allowed_prefixes = [
#                 "/",
#                 "/results/",
#                 "/centers/",
#                 "/seats/",
#                 "/dashboard/",
#             ]

#             if any(path.startswith(p) for p in allowed_prefixes):
#                 return self.get_response(request)

#             return render(request, "core/access_denied.html")

#         return self.get_response(request)

from django.shortcuts import redirect

class RoleAccessMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path
        user = request.user

        # =========================
        # 🔓 ROUTES LIBRES (IMPORTANT)
        # =========================
        public_paths = [
            "/accounts/login/",
            "/accounts/register/",
            "/accounts/logout/",
            "/accounts/appeal/",
            "/admin/",  # Django admin
            "/access-denied/",
        ]

        if any(path.startswith(p) for p in public_paths):
            return self.get_response(request)
        
        # =========================
        # 🚫 UTILISATEUR SUSPENDU
        # =========================
        if user.is_authenticated and user.is_suspended:
    
            # autoriser uniquement appeal + logout
            if path.startswith("/accounts/appeal/") or path.startswith("/accounts/logout/"):
                return self.get_response(request)

            return redirect("appeal")

        # fichiers statiques
        if path.startswith("/static/"):
            return self.get_response(request)

        # =========================
        # 🔐 NON CONNECTÉ
        # =========================
        if not user.is_authenticated:
            return redirect("login")

        # =========================
        # 👑 ADMIN
        # =========================
        if user.role == "ADMIN":
            return self.get_response(request)

        # =========================
        # 👮 AGENT
        # =========================
        if user.role == "AGENT":

            allowed_paths = [
                "/",  # 🔥 dashboard corrigé
                "/agent/",
                "/results/",
                "/centers/",
                "/seats/",
            ]

            if any(path.startswith(p) for p in allowed_paths):
                return self.get_response(request)

            return redirect("access_denied")

        # =========================
        # 👤 ELECTEUR
        # =========================
        if user.role == "ELECTEUR":

            allowed_paths = [
                "/",  # 🔥 dashboard
                "/results/",
                "/centers/",
                "/seats/",
            ]

            if any(path.startswith(p) for p in allowed_paths):
                return self.get_response(request)

            return redirect("access_denied")

        return self.get_response(request)