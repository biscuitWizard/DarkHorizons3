using System;
using System.Collections.Generic;
using System.IO;

using NDesk.Options;

namespace Aurora
{
    class Program
    {
        public enum StartupOption
        {
            None,
            StartGame,
            StopGame,
            MigrateData,
            ShowHelp,
            CreateGame
        }

        [STAThread]
        static void Main(string[] args)
        {
            string newGameName = string.Empty;
            StartupOption startupAction = StartupOption.None;
            var options = new OptionSet
                {
                    {"i|init", "Initiaize a new game.", i => { newGameName = i; startupAction =  StartupOption.CreateGame; }},
                    {"start", "Start the server for the game in the current directory.", s => startupAction = s != null ? StartupOption.StartGame : startupAction},
                    {"stop", "Stop the server for the game in the current directory.", s => startupAction = s != null ? StartupOption.StopGame : startupAction},
                    {"migrate", "Migrate the server data for the game in the current directory.", s => startupAction = s != null ? StartupOption.MigrateData : startupAction},
                    {"h|help", "Show this help file.", s => startupAction = s != null ? StartupOption.ShowHelp : startupAction}
                };

            List<string> extra;
            try
            {
                extra = options.Parse(args);
                if (startupAction == StartupOption.None)
                {
                    ShowHelp(options);
                    return;
                }
            }
            catch (OptionException e)
            {
                Console.Write("Aurora: ");
                Console.WriteLine(e.Message);
                Console.WriteLine("Try `aurora --help' for more information.");
                return;
            }

            var workingDirectory = Directory.GetCurrentDirectory();
            Console.WriteLine("Directory: {0}", workingDirectory);
            switch (startupAction)
            {
                case StartupOption.ShowHelp:
                    ShowHelp(options);
                    break;
                default:
                    break;
            }
        }

        static void ShowHelp(OptionSet p)
        {
            Console.WriteLine("Usage: aurora [OPTIONS]+");
            Console.WriteLine("Manage Aurora MU* Game Servers");
            Console.WriteLine();
            Console.WriteLine("Options:");
            p.WriteOptionDescriptions(Console.Out);
        }
    }
}
