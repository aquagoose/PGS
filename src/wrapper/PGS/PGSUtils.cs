using System;
using System.Collections.Generic;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;

namespace PRS
{
    public static class PGSUtils
    {
        public static void SetTexturePixels(ref Texture2D targetTexture, Color[] colors)
        {
            targetTexture.SetData(colors);
        }
    }
}