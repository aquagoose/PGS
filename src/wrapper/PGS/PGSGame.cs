using System;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

namespace PRS
{
    public class PGSGame : Game
    {
        public event GameInitialize InitializeEvent;
        public event GameUpdate UpdateEvent;
        public event GameDraw DrawEvent;

        protected override void Initialize()
        {
            InitializeEvent?.Invoke();

            base.Initialize();
        }

        protected override void Update(GameTime gameTime)
        {
            UpdateEvent?.Invoke(gameTime);

            base.Update(gameTime);
        }

        protected override void Draw(GameTime gameTime)
        {
            DrawEvent?.Invoke();

            base.Draw(gameTime);
        }

        public delegate void GameInitialize();
        public delegate void GameUpdate(GameTime gameTime);
        public delegate void GameDraw();
    }
}
