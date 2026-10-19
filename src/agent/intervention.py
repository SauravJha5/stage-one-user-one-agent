import csv
from typing import List, Dict, Any
from src.models import ViewerState

class InterventionPlanner:
    def __init__(self, catalogue_path: str = "data/catalogue.csv"):
        self.catalogue: List[Dict[str, Any]] = []
        with open(catalogue_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.catalogue.append(row)

    def get_content_for_dialect(self, dialect: str, limit: int = 3) -> List[str]:
        selected = []
        seen_slugs = set()

        for item in self.catalogue:
            # Trap: Sirf matching dialect aur available content
            if item.get("dialect") == dialect:
                slug = item.get("content_slug")
                if slug and slug in seen_slugs:
                    continue  # Deduplicate same slug variants
                
                title_id = item.get("title_id")
                # Title ko pick karein, description mein fake instruction ho toh bhi ignore ho jata hai
                selected.append(f"title:{title_id}")
                if slug:
                    seen_slugs.add(slug)
                if len(selected) >= limit:
                    break
        return selected

    def plan_action(self, state: ViewerState, chosen_dialect: str) -> Dict[str, Any]:
        # Default policy: App open hone par pehle Home Page curate karo
        content = self.get_content_for_dialect(chosen_dialect, limit=3)
        if len(content) < 3:
            return {"action": "NO_ACTION", "content": [], "reason": "Insufficient content in dialect"}

        return {
            "action": "HOME_PAGE",
            "content": content,
            "reason": f"Curated {len(content)} titles for dialect {chosen_dialect}"
        }
