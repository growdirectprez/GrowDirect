<?xml version='1.0'?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/TR/WD-xsl">

   <!-- Match the root node -->
   <xsl:template match="/">
      <xsl:apply-templates select="*"/>
   </xsl:template>

   <!-- Match everything else -->
   <xsl:template match="*|@*|text()|cdata()|comment()|pi()">

      <xsl:copy>
         <xsl:apply-templates order-by="+ @Evt_Type_SortValue; + @Dept; + @Cat; - @On_Promo; + @SKU" select="*|@*|text()|cdata()|comment()|pi()">
         </xsl:apply-templates>
      </xsl:copy>

   </xsl:template>
</xsl:stylesheet>


