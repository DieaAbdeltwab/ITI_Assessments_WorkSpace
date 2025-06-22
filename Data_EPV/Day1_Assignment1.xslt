<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:template match="/students">
    <!-- CSV Header -->
    SID,First Name,Last Name,Date
    <br/>
    <xsl:for-each select="student">
      <xsl:value-of select="@SID"/>,
      <xsl:value-of select="firstName"/>,
      <xsl:value-of select="lastName"/>,
      <xsl:value-of select="date"/>
    <br/>
    </xsl:for-each>
  </xsl:template>

</xsl:stylesheet>
