using System;

namespace Aurora
{
    public static class DateTimeExensions
    {
        private static readonly DateTime UnixMinTime = new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc);

        public static double ToSeconds(this DateTime dateTime)
        {
            TimeSpan span = dateTime.Subtract(UnixMinTime);
            return span.TotalSeconds;
        }
    }
}
