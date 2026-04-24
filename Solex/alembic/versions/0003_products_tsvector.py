"""products tsvector"""
from alembic import op

revision = "0003"
down_revision = "7ddc249fe44d"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE products ADD COLUMN search_tsv tsvector;")
    op.execute("CREATE INDEX ix_products_search_tsv ON products USING GIN (search_tsv);")
    op.execute("""
        CREATE FUNCTION products_tsv_update() RETURNS trigger AS $$
        BEGIN
          NEW.search_tsv :=
            setweight(to_tsvector('english', coalesce(NEW.name,'')), 'A') ||
            setweight(to_tsvector('english', coalesce(NEW.short_description,'')), 'B') ||
            setweight(to_tsvector('english', coalesce(NEW.description,'')), 'C') ||
            setweight(to_tsvector('english', coalesce(NEW.sku,'')), 'A');
          RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
    """)
    op.execute("""
        CREATE TRIGGER products_tsv_trigger
          BEFORE INSERT OR UPDATE ON products
          FOR EACH ROW EXECUTE FUNCTION products_tsv_update();
    """)
    op.execute("UPDATE products SET id = id;")


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS products_tsv_trigger ON products;")
    op.execute("DROP FUNCTION IF EXISTS products_tsv_update;")
    op.execute("DROP INDEX IF EXISTS ix_products_search_tsv;")
    op.execute("ALTER TABLE products DROP COLUMN IF EXISTS search_tsv;")
