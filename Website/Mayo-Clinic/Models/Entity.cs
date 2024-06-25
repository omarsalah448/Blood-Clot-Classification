using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace Mayo_Clinic.Models
{
    public class Entity : IdentityDbContext<ApplicationUser>
    {
        public Entity(DbContextOptions options) : base(options)
        {
            
        }
        public DbSet<Doctor> Doctors { get; set; }
        public DbSet<Patient> Patients { get; set; }
    }
}
