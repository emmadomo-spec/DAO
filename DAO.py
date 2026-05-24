import sqlite3
from typing import Protocol

from Models.data import (
    UserDTO,
    EtudiantDTO,
    EnseignantDTO,
    PromotionDTO,
    UniteEnseignementDTO,
    CoursDTO,
    SeanceDTO,
)


class BaseDatabase:
    def __init__(self, db_file: str = "app_storage.db"):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self._initialize_schema()

    def _initialize_schema(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            create table if not exists users (
                id integer primary key,
                role text,
                email text,
                google_linked boolean
            )
        """)

        cursor.execute("""
            create table if not exists promotions (
                id_promotion integer primary key,
                nom_promotion text,
                annee_academique text
            )
        """)

        cursor.execute("""
            create table if not exists etudiants (
                id_etudiant integer primary key,
                matricule text,
                nom text,
                prenom text,
                email text,
                id_promotion integer
            )
        """)

        cursor.execute("""
            create table if not exists enseignants (
                id_enseignant integer primary key,
                nom text,
                prenom text,
                email text,
                id_ue integer
            )
        """)

        cursor.execute("""
            create table if not exists unites_enseignement (
                id_ue integer primary key,
                code_ue text,
                intitule text,
                credits_ects integer,
                id_promotion integer
            )
        """)

        cursor.execute("""
            create table if not exists cours (
                id_cours integer primary key,
                intitule text,
                volume_horaire integer,
                id_ue integer
            )
        """)

        cursor.execute("""
            create table if not exists seances (
                id_seance integer primary key,
                titre text,
                date text,
                heure_debut text,
                heure_fin text,
                salle text,
                status_synchro text,
                type text,
                id_cours integer
            )
        """)

        self.connection.commit()


class RepositoryInterface(Protocol):
    def find_by_id(self, identifier): ...
    def find_all(self): ...
    def insert_or_update(self, entity): ...
    def remove(self, identifier): ...


class UserRepository(BaseDatabase):
    def find_all(self):
        cursor = self.connection.cursor()
        dataset = cursor.execute("select * from users").fetchall()
        return [
            UserDTO(
                id=record["id"],
                role=record["role"],
                email=record["email"],
                google_linked=bool(record["google_linked"])
            )
            for record in dataset
        ]

    def find_by_id(self, identifier):
        cursor = self.connection.cursor()
        record = cursor.execute("select * from users where id = ?", (identifier,)).fetchone()
        
        if record is None:
            return None
            
        return UserDTO(
            id=record["id"],
            role=record["role"],
            email=record["email"],
            google_linked=bool(record["google_linked"])
        )

    def insert_or_update(self, user: UserDTO):
        cursor = self.connection.cursor()
        cursor.execute(
            "insert or replace into users values (?, ?, ?, ?)",
            (user.id, user.role, user.email, int(user.google_linked))
        )
        self.connection.commit()

    def remove(self, identifier):
        cursor = self.connection.cursor()
        cursor.execute("delete from users where id = ?", (identifier,))
        self.connection.commit()

    def find_by_email(self, email_address):
        cursor = self.connection.cursor()
        record = cursor.execute("select * from users where email = ?", (email_address,)).fetchone()
        
        if record is None:
            return None
            
        return UserDTO(
            id=record["id"],
            role=record["role"],
            email=record["email"],
            google_linked=bool(record["google_linked"])
        )


class StudentRepository(BaseDatabase):
    def find_all(self):
        cursor = self.connection.cursor()
        dataset = cursor.execute("select * from etudiants").fetchall()
        return [
            EtudiantDTO(
                id_etudiant=row["id_etudiant"],
                matricule=row["matricule"],
                nom=row["nom"],
                prenom=row["prenom"],
                email=row["email"],
                id_promotion=row["id_promotion"]
            ) for row in dataset
        ]

    def find_by_id(self, identifier):
        cursor = self.connection.cursor()
        row = cursor.execute("select * from etudiants where id_etudiant = ?", (identifier,)).fetchone()
        
        if row is None:
            return None
            
        return EtudiantDTO(
            id_etudiant=row["id_etudiant"],
            matricule=row["matricule"],
            nom=row["nom"],
            prenom=row["prenom"],
            email=row["email"],
            id_promotion=row["id_promotion"]
        )

    def insert_or_update(self, student: EtudiantDTO):
        cursor = self.connection.cursor()
        cursor.execute(
            "insert or replace into etudiants values (?, ?, ?, ?, ?, ?)",
            (student.id_etudiant, student.matricule, student.nom, student.prenom, student.email, student.id_promotion)
        )
        self.connection.commit()

    def remove(self, identifier):
        cursor = self.connection.cursor()
        cursor.execute("delete from etudiants where id_etudiant = ?", (identifier,))
        self.connection.commit()

    def find_by_class(self, promotion_id):
        cursor = self.connection.cursor()
        dataset = cursor.execute("select * from etudiants where id_promotion = ?", (promotion_id,)).fetchall()
        return [
            EtudiantDTO(
                id_etudiant=row["id_etudiant"],
                matricule=row["matricule"],
                nom=row["nom"],
                prenom=row["prenom"],
                email=row["email"],
                id_promotion=row["id_promotion"]
            ) for row in dataset
        ]


class TeacherRepository(BaseDatabase):
    def find_all(self):
        cursor = self.connection.cursor()
        dataset = cursor.execute("select * from enseignants").fetchall()
        return [
            EnseignantDTO(
                id_enseignant=row["id_enseignant"],
                nom=row["nom"],
                prenom=row["prenom"],
                email=row["email"],
                id_ue=row["id_ue"]
            ) for row in dataset
        ]

    def find_by_id(self, identifier):
        cursor = self.connection.cursor()
        row = cursor.execute("select * from enseignants where id_enseignant = ?", (identifier,)).fetchone()
        
        if row is None:
            return None
            
        return EnseignantDTO(
            id_enseignant=row["id_enseignant"],
            nom=row["nom"],
            prenom=row["prenom"],
            email=row["email"],
            id_ue=row["id_ue"]
        )

    def insert_or_update(self, teacher: EnseignantDTO):
        cursor = self.connection.cursor()
        cursor.execute(
            "insert or replace into enseignants values (?, ?, ?, ?, ?)",
            (teacher.id_enseignant, teacher.nom, teacher.prenom, teacher.email, teacher.id_ue)
        )
        self.connection.commit()

    def remove(self, identifier):
        cursor = self.connection.cursor()
        cursor.execute("delete from enseignants where id_enseignant = ?", (identifier,))
        self.connection.commit()

    def find_by_course_unit(self, ue_id):
        cursor = self.connection.cursor()
        dataset = cursor.execute("select * from enseignants where id_ue = ?", (ue_id,)).fetchall()
        return [
            EnseignantDTO(
                id_enseignant=row["id_enseignant"],
                nom=row["nom"],
                prenom=row["prenom"],
                email=row["email"],
                id_ue=row["id_ue"]
            ) for row in dataset
        ]


class BatchRepository(BaseDatabase):
    def find_all(self):
        cursor = self.connection.cursor()
        dataset = cursor.execute("select * from promotions").fetchall()
        return [
            PromotionDTO(
                id_promotion=row["id_promotion"],
                nom_promotion=row["nom_promotion"],
                annee_academique=row["annee_academique"]
            ) for row in dataset
        ]

    def find_by_id(self, identifier):
        cursor = self.connection.cursor()
        row = cursor.execute("select * from promotions where id_promotion = ?", (identifier,)).fetchone()
        
        if row is None:
            return None
            
        return PromotionDTO(
            id_promotion=row["id_promotion"],
            nom_promotion=row["nom_promotion"],
            annee_academique=row["annee_academique"]
        )

    def insert_or_update(self, batch: PromotionDTO):
        cursor = self.connection.cursor()
        cursor.execute(
            "insert or replace into promotions values (?, ?, ?)",
            (batch.id_promotion, batch.nom_promotion, batch.annee_academique)
        )
        self.connection.commit()

    def remove(self, identifier):
        cursor = self.connection.cursor()
        cursor.execute("delete from promotions where id_promotion = ?", (identifier,))
        self.connection.commit()


class CourseUnitRepository(BaseDatabase):
    def find_all(self):
        cursor = self.connection.cursor()
        dataset = cursor.execute("select * from unites_enseignement").fetchall()
        return [
            UniteEnseignementDTO(
                id_ue=row["id_ue"],
                code_ue=row["code_ue"],
                intitule=row["intitule"],
                credits_ects=row["credits_ects"],
                id_promotion=row["id_promotion"]
            ) for row in dataset
        ]

    def find_by_id(self, identifier):
        cursor = self.connection.cursor()
        row = cursor.execute("select * from unites_enseignement where id_ue = ?", (identifier,)).fetchone()
        
        if row is None:
            return None
            
        return UniteEnseignementDTO(
            id_ue=row["id_ue"],
            code_ue=row["code_ue"],
            intitule=row["intitule"],
            credits_ects=row["credits_ects"],
            id_promotion=row["id_promotion"]
        )

    def insert_or_update(self, ue: UniteEnseignementDTO):
        cursor = self.connection.cursor()
        cursor.execute(
            "insert or replace into unites_enseignement values (?, ?, ?, ?, ?)",
            (ue.id_ue, ue.code_ue, ue.intitule, ue.credits_ects, ue.id_promotion)
        )
        self.connection.commit()

    def remove(self, identifier):
        cursor = self.connection.cursor()
        cursor.execute("delete from unites_enseignement where id_ue = ?", (identifier,))
        self.connection.commit()

    def find_by_batch(self, promotion_id):
        cursor = self.connection.cursor()
        dataset = cursor.execute("select * from unites_enseignement where id_promotion = ?", (promotion_id,)).fetchall()
        return [
            UniteEnseignementDTO(
                id_ue=row["id_ue"],
                code_ue=row["code_ue"],
                intitule=row["intitule"],
                credits_ects=row["credits_ects"],
                id_promotion=row["id_promotion"]
            ) for row in dataset
        ]


class CourseRepository(BaseDatabase):
    def find_all(self):
        cursor = self.connection.cursor()
        dataset = cursor.execute("select * from cours").fetchall()
        return [
            CoursDTO(
                id_cours=row["id_cours"],
                intitule=row["intitule"],
                volume_horaire=row["volume_horaire"],
                id_ue=row["id_ue"]
            ) for row in dataset
        ]

    def find_by_id(self, identifier):
        cursor = self.connection.cursor()
        row = cursor.execute("select * from cours where id_cours = ?", (identifier,)).fetchone()
        
        if row is None:
            return None
            
        return CoursDTO(
            id_cours=row["id_cours"],
            intitule=row["intitule"],
            volume_horaire=row["volume_horaire"],
            id_ue=row["id_ue"]
        )

    def insert_or_update(self, course: CoursDTO):
        cursor = self.connection.cursor()
        cursor.execute(
            "insert or replace into cours values (?, ?, ?, ?)",
            (course.id_cours, course.intitule, course.volume_horaire, course.id_ue)
        )
        self.connection.commit()

    def remove(self, identifier):
        cursor = self.connection.cursor()
        cursor.execute("delete from cours where id_cours = ?", (identifier,))
        self.connection.commit()

    def find_by_course_unit(self, ue_id):
        cursor = self.connection.cursor()
        dataset = cursor.execute("select * from cours where id_ue = ?", (ue_id,)).fetchall()
        return [
            CoursDTO(
                id_cours=row["id_cours"],
                intitule=row["intitule"],
                volume_horaire=row["volume_horaire"],
                id_ue=row["id_ue"]
            ) for row in dataset
        ]


class CalendarEventRepository(BaseDatabase):
    def find_all(self):
        cursor = self.connection.cursor()
        dataset = cursor.execute("select * from seances").fetchall()
        return [
            SeanceDTO(
                id_seance=row["id_seance"],
                titre=row["titre"],
                date=row["date"],
                heure_debut=row["heure_debut"],
                heure_fin=row["heure_fin"],
                salle=row["salle"],
                status_synchro=row["status_synchro"],
                type=row["type"],
                id_cours=row["id_cours"]
            ) for row in dataset
        ]

    def find_by_id(self, identifier):
        cursor = self.connection.cursor()
        row = cursor.execute("select * from seances where id_seance = ?", (identifier,)).fetchone()
        
        if row is None:
            return None
            
        return SeanceDTO(
            id_seance=row["id_seance"],
            titre=row["titre"],
            date=row["date"],
            heure_debut=row["heure_debut"],
            heure_fin=row["heure_fin"],
            salle=row["salle"],
            status_synchro=row["status_synchro"],
            type=row["type"],
            id_cours=row["id_cours"]
        )

    def insert_or_update(self, event: SeanceDTO):
        cursor = self.connection.cursor()
        cursor.execute(
            "insert or replace into seances values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                event.id_seance,
                event.titre,
                event.date,
                event.heure_debut,
                event.heure_fin,
                event.salle,
                event.status_synchro,
                event.type,
                event.id_cours
            )
        )
        self.connection.commit()

    def remove(self, identifier):
        cursor = self.connection.cursor()
        cursor.execute("delete from seances where id_seance = ?", (identifier,))
        self.connection.commit()

    def find_by_course(self, course_id):
        cursor = self.connection.cursor()
        dataset = cursor.execute("select * from seances where id_cours = ?", (course_id,)).fetchall()
        return [
            SeanceDTO(
                id_seance=row["id_seance"],
                titre=row["titre"],
                date=row["date"],
                heure_debut=row["heure_debut"],
                heure_fin=row["heure_fin"],
                salle=row["salle"],
                status_synchro=row["status_synchro"],
                type=row["type"],
                id_cours=row["id_cours"]
            ) for row in dataset
        ]

    def find_by_timeline(self, start_date, end_date):
        cursor = self.connection.cursor()
        dataset = cursor.execute("select * from seances where date between ? and ?", (start_date, end_date)).fetchall()
        return [
            SeanceDTO(
                id_seance=row["id_seance"],
                titre=row["titre"],
                date=row["date"],
                heure_debut=row["heure_debut"],
                heure_fin=row["heure_fin"],
                salle=row["salle"],
                status_synchro=row["status_synchro"],
                type=row["type"],
                id_cours=row["id_cours"]
            ) for row in dataset
        ]

    def refresh_sync_status(self, id_seance, status):
        cursor = self.connection.cursor()
        cursor.execute("update seances set status_synchro = ? where id_seance = ?", (status, id_seance))
        self.connection.commit()
