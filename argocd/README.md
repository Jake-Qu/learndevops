argocd app create argocd --repo https://github.com/Jake-Qu/learndevops.git --path argocd/resources/ --dest-server https://kubernetes.default.svc --dest-namespace argocd --sync-policy auto
