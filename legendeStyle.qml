<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="2.0.1-Dufour" minimumScale="-4.65661e-10" maximumScale="1e+08" simplifyDrawingHints="0" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
  <renderer-v2 symbollevels="0" type="RuleRenderer">
    <rules key="{c36405c1-51be-4316-8421-193c3bfa4c8d}">
      <rule filter=" &quot;SECT&quot; ='1'" key="{dd522d70-c92a-49fc-ac15-717e8d822a84}" symbol="0"/>
      <rule filter=" &quot;SECT&quot; not in ('1', 'L')" key="{d377501c-b5fc-4be8-bcd2-9d1c99a67478}" symbol="1"/>
      <rule filter="&quot;SECT&quot; = 'L'" key="{010cf040-9378-49a3-97a6-6b086d03ef32}" symbol="2"/>
    </rules>
    <symbols>
      <symbol alpha="1" clip_to_extent="1" type="fill" name="0">
        <layer pass="2" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="240,240,240,255"/>
          <prop k="color_border" v="0,0,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="fill" name="1">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="7,178,175,255"/>
          <prop k="color_border" v="255,255,255,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="no"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.1"/>
        </layer>
        <layer pass="1" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="0,0,255,255"/>
          <prop k="color_border" v="0,0,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="no"/>
          <prop k="style_border" v="dash"/>
          <prop k="width_border" v="0.1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="fill" name="2">
        <layer pass="3" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="178,58,180,255"/>
          <prop k="color_border" v="0,0,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="no"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.1"/>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <customproperties>
    <property key="labeling" value="pal"/>
    <property key="labeling/addDirectionSymbol" value="false"/>
    <property key="labeling/dataDefined/Show" value="1~~1~~&quot;SECT&quot; = '1'~~"/>
    <property key="labeling/displayAll" value="true"/>
    <property key="labeling/enabled" value="true"/>
    <property key="labeling/dataDefined/OffsetXY" value="1~~0~~~~POS_LEG"/>
    <property key="labeling/labelOffsetInMapUnits" value="true"/>
    <property key="labeling/fieldName" value=" format_number( VAL,0)"/>
    <property key="labeling/fontSize" value="10"/>
    <property key="labeling/fontSizeInMapUnits" value="false"/>
    <property key="labeling/isExpression" value="true"/>
    <property key="labeling/placement" value="1"/>
  </customproperties>
</qgis>
