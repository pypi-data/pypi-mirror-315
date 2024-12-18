import unittest
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get the absolute path to the project root directory
project_root = Path(__file__).parent

# Add project root to Python path
sys.path.append(str(project_root))

# Import the SDK package
from src.python.client import NewscatcherApi
from src.python.environment import NewscatcherApiEnvironment
from pydantic import ValidationError


class TestNewsCatcherSDK(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        api_key = os.getenv("NEWSCATCHER_API_KEY_V3")
        if not api_key:
            raise ValueError("NEWSCATCHER_API_KEY_V3 not found in .env file")

        print(f"Initializing client with API key: {api_key[:5]}...")
        try:
            cls.client = NewscatcherApi(
                api_key=api_key, environment=NewscatcherApiEnvironment.DEFAULT
            )
        except Exception as e:
            print(f"Failed to initialize client: {str(e)}")
            raise

    def verify_article_response(self, articles):
        """Helper method to verify article response structure"""
        for article in articles:
            self.assertIsInstance(article.title, str, "Title should be a string")
            if hasattr(article, "is_headline"):
                self.assertIsInstance(
                    article.is_headline, bool, "is_headline should be a boolean"
                )

    def test_search(self):
        """Test the search endpoint"""
        try:
            response = self.client.search.post(
                q="artificial intelligence",
                lang="en",
                countries="US",
                from_="7d",
                page_size=10,
                sort_by="relevancy",
                ranked_only=True,
            )

            self.assertIsNotNone(response)
            self.assertTrue(hasattr(response, "articles"))
            self.assertLessEqual(len(response.articles), 10)
            self.verify_article_response(response.articles)

            print(f"\nFound {len(response.articles)} articles")
            if response.articles:
                print(f"First article title: {response.articles[0].title}")

        except Exception as e:
            self.fail(f"Search test failed with error: {str(e)}")

    def test_latest_headlines(self):
        """Test the latest headlines endpoint"""
        try:
            response = self.client.latestheadlines.post(
                when="7d", lang="en", countries="US", page_size=10, ranked_only=True
            )

            self.assertIsNotNone(response)
            self.assertTrue(hasattr(response, "articles"))
            article_count = len(response.articles)
            self.assertGreater(article_count, 0, "No articles found")
            self.verify_article_response(response.articles)

            print(f"\nFound {article_count} latest headlines")
            if response.articles:
                print(f"First headline title: {response.articles[0].title}")

        except Exception as e:
            self.fail(f"Latest headlines test failed with error: {str(e)}")

    def test_authors(self):
        """Test the authors endpoint"""
        try:
            response = self.client.authors.post(
                author_name="John Smith",
                lang="en",
                countries="US",
                page_size=10,
                from_="7d",
                ranked_only=True,
            )

            self.assertIsNotNone(response)
            self.assertTrue(hasattr(response, "articles"))
            print(f"\nFound {len(response.articles)} articles by author")

        except Exception as e:
            self.fail(f"Authors test failed with error: {str(e)}")

    def test_search_similar(self):
        """Test the search similar articles endpoint"""
        try:
            response = self.client.searchsimilar.post(
                q="artificial intelligence",
                search_in="title,content",
                lang="en",
                countries="US",
                page_size=10,
                include_similar_documents=True,
                similar_documents_number=5,
                ranked_only=True,
            )

            self.assertIsNotNone(response)
            self.assertTrue(hasattr(response, "articles"))
            self.verify_article_response(response.articles)
            print(f"\nFound {len(response.articles)} similar articles")

        except Exception as e:
            self.fail(f"Search similar test failed with error: {str(e)}")

    def test_search_by_link(self):
        """Test the search by link endpoint"""
        try:
            # First get an article URL from search
            search_response = self.client.search.post(
                q="artificial intelligence", lang="en", page_size=1
            )

            if search_response.articles and len(search_response.articles) > 0:
                article_link = search_response.articles[0].link
                from src.python.searchlink.types.search_link_post_request_links import (
                    SearchLinkPostRequestLinks,
                )

                # Create request using string URL directly
                request_data = SearchLinkPostRequestLinks(
                    links=article_link, from_="1 month ago"  # Pass link directly
                )

                response = self.client.searchlink.post(request=request_data)

                self.assertIsNotNone(response)
                self.assertTrue(hasattr(response, "articles"))
                print(f"\nFound {len(response.articles)} articles by link")
                if response.articles:
                    print(f"Article title: {response.articles[0].title}")

        except Exception as e:
            self.fail(f"Search by link test failed with error: {str(e)}")

    def test_aggregation(self):
        """Test the aggregation endpoint"""
        try:
            response = self.client.aggregation.post(
                q="artificial intelligence",
                lang="en",
                countries="US",
                from_="7d",
                aggregation_by="day",  # Aggregate by day
            )

            self.assertIsNotNone(response)
            # Check for top-level response structure
            self.assertTrue(
                hasattr(response, "status") or hasattr(response, "total_hits")
            )

            # Access aggregations data, which might be in different formats
            if hasattr(response, "aggregations"):
                aggregations = response.aggregations
            else:
                # If aggregations is directly in the response
                aggregations = getattr(response, "user_input", [])

            # Print aggregation information
            print(f"\nAggregation response received")
            print(f"Status: {getattr(response, 'status', 'N/A')}")

            # If there are aggregated results, show first one
            if aggregations and len(aggregations) > 0:
                print(f"First aggregation entry: {aggregations[0]}")

        except Exception as e:
            self.fail(f"Aggregation test failed with error: {str(e)}")

        except Exception as e:
            self.fail(f"Aggregation test failed with error: {str(e)}")

    def test_sources(self):
        """Test the sources endpoint"""
        try:
            response = self.client.sources.post(lang="en", countries="US")

            self.assertIsNotNone(response)
            self.assertTrue(hasattr(response, "sources"))
            print(f"\nFound {len(response.sources)} sources")

        except Exception as e:
            self.fail(f"Sources test failed with error: {str(e)}")

    def test_subscription(self):
        """Test the subscription endpoint"""
        try:
            response = self.client.subscription.get()

            self.assertIsNotNone(response)
            self.assertTrue(hasattr(response, "active"))
            self.assertTrue(hasattr(response, "plan"))
            print(f"\nSubscription plan: {response.plan}")

        except Exception as e:
            self.fail(f"Subscription test failed with error: {str(e)}")


def main():
    # Set up test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNewsCatcherSDK)

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    main()
